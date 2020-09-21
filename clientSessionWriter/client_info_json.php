<?php
/**
 * client infomation for wemakeprice corp.
 *
 * @author Hasoo Kim <vaxzeem@i-heart.co.kr>
 */

header("Content-Type: application/json; charset=utf-8"); 

$shm_client = @shmop_open(0x1212, "a", 0644, 100);
$record_cnt = 2000;

$shm_size = @shmop_size($shm_client);
$record_size = $shm_size / $record_cnt;

$physicalPack = "a20groupId/a20clientId/a1lineType/i1pid/a16clientIp/i1clientPort/i1connectDate/i1updateDate/i1todaySentSms/i1todaySentMms/i1recentSmsMin0/i1recentSmsMin1/i1recentSmsMin2/i1recentSmsMin3/i1recentSmsMin4/i1recentSmsMin5/i1recentSmsMin6/i1recentSmsMin7/i1recentSmsMin8/i1recentSmsMin9/i1recentMmsMin0/i1recentMmsMin1/i1recentMmsMin2/i1recentMmsMin3/i1recentMmsMin4/i1recentMmsMin5/i1recentMmsMin6/i1recentMmsMin7/i1recentMmsMin8/i1recentMmsMin9";

$my_string = @shmop_read($shm_client, 0, $shm_size);

$json = '{';

$json .= '"info":[';
$isFirstLine = true;
for ($i = 0; $i < $record_cnt; ++$i) {
	$sub = @substr($my_string, $i * $record_size, $record_size);
	$clientsInfo = @unpack($physicalPack, $sub);
	
	if ("" == $clientsInfo['clientId']) break;
	if ("M" == @trim($clientsInfo['lineType'])) continue;

	if($isFirstLine) {
		$json .= '{';
		$isFirstLine = false;
	}
	else {
		$json .= ',{';
	}

	$json .= '"pid":' . '"' . $clientsInfo['pid'] . '",';
	$json .= '"groupId":' . '"' . $clientsInfo['groupId'] . '",';
	$json .= '"clientId":' . '"' . $clientsInfo['clientId'] . '",';
	$json .= '"lineType":' . '"' . $clientsInfo['lineType'] . '",';
	$json .= '"ip":' . '"' . $clientsInfo['clientIp'] . '",';
	$json .= '"date":' . '"' . date('Y-m-d H:i:s', $clientsInfo['connectDate']) . '"';

	$json .= '}';
}
$json .= '],';

$json .= '"session":[';
$isFirstLine = true;
$singleWorker = shell_exec('ps -ef | grep SingleWorker | grep -v grep | awk \'{printf "%s %s %s\n",$2,$9,$10}\''); 
$clientSession = explode("\n", $singleWorker);
foreach($clientSession as $line) {	
	if ('' == $line) continue;

	$clientsInfo = explode(" ", $line);
	if($isFirstLine) {
		$json .= '{';
		$isFirstLine = false;
	}
	else {
		$json .= ',{';
	}
	$json .= '"pid":' . '"' . $clientsInfo[0] . '",';
	$json .= '"clientId":' . '"' . $clientsInfo[1] . '",';
	$json .= '"lineType":' . '"' . $clientsInfo[2] . '"';
	$json .= '}';
}
$json .= ']';

$json .= '}';
echo $json;

@shmop_close($shm_client);
?>
