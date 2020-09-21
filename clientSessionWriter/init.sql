create table client_session
(
 group_id varchar2(20),
 client_id varchar2(20),
 line_type varchar2(10),
 pid varchar2(10),
 ip varchar2(20),
 connected_date varchar2(20),
 system_id varchar2(10)
);

create index ix1_client_session on client_session(client_id,pid);
create index ix2_client_session on client_session(group_id, client_id, line_type);
alter table client_session add(system_id varchar2(20));