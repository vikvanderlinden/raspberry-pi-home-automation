<?php

function top($title) {
	include_once "partials/top.php";
	echo $title;
	include_once "partials/middle.php";
}

function bottom() {
	include_once "partials/bottom.php";
}

function navigation() {
	include_once "partials/navigation.php";
}

?>
