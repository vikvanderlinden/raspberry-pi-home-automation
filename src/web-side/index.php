<?php

$DB = new PDO('mysql:host=127.0.0.1;dbname=testdb', 'root', 'RaspberryVV');

$temperatures = $DB->query("(SELECT * FROM temperatures ORDER BY time DESC LIMIT 60) ORDER BY time ASC");

$DB = null;

?>
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

	<title>LAN RP Server</title>
</head>
<body>
	<nav class="navbar navbar-expand-lg navbar-light bg-light">
		<a class="navbar-brand" href="#">LAN RP Server</a>
		<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
			<span class="navbar-toggler-icon"></span>
		</button>

		<div class="collapse navbar-collapse" id="navbarSupportedContent">
			<ul class="navbar-nav mr-auto">
				<li class="nav-item active">
					<a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
				</li>
				<li class="nav-item">
					<a class="nav-link" href="#">Stats</a>
				</li>
				<li class="nav-item dropdown">
					<a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Controls</a>
					<div class="dropdown-menu" aria-labelledby="navbarDropdown">
						<a class="dropdown-item" href="#">Edit actions</a>
						<a class="dropdown-item" href="#">Add actions</a>
						<div class="dropdown-divider"></div>
						<a class="dropdown-item" href="#">Plan actions</a>
					</div>
				</li>
				<li class="nav-item">
					<a class="nav-link disabled" href="#">Visualized</a>
				</li>
			</ul>
			<form class="form-inline my-2 my-lg-0">
				<input class="form-control mr-sm-2" type="search" placeholder="What are you looking for?" aria-label="Search">
				<button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
			</form>
		</div>
	</nav>
	<br>
	<div class="container">
		<div class="jumbotron">
			<h1 class="display-3">Raspberry Pi webserver</h1>
			<p class="lead">This website is hosted on the Raspberry Pi. Interaction between the raspberry pi's action schedule will be implemented here.</p>
			<hr class="my-4">
			<p>This site uses database information that is directly stored on the Raspberry Pi! In case the Pi adds information, that will be directly visible here.</p>
			<p class="lead">
				<a class="btn btn-primary btn-lg" href="#" role="button">Learn more</a>
			</p>
		</div>
		<h2 class="display-4">The temperatures:</h2>
		<table class="table">
			<thead>
				<tr>
					<th scope="col">#</th>
					<th scope="col">Temperature (°C)</th>
					<th scope="col">Time</th>
					<th scope="col">Note</th>
				</tr>
			</thead>
			<tbody>
			<?php $times = []; $temps = []; foreach ($temperatures as $temperature) { ?>
				<tr>
					<th scope="row"><?php echo $temperature['id']; ?></th>
					<td><?php echo $temperature['temperature']; ?></td>
					<td><?php echo date("d/m/'y H:i:s", strtotime($temperature['time'])); ?></td>
					<td><?php echo $temperature['note']; ?></td>
				</tr>
			<?php
			$times[] = date("Y-m-d H:i:s", strtotime($temperature['time']));
			$temps[] = floatval($temperature['temperature']);
			} ?>
			</tbody>
		</table>
		<hr>
		<h2 class="display-4">The graph:</h2>
		<canvas id="myChart" times='<?= json_encode($times); ?>' temps='<?= json_encode($temps) ?>'></canvas>
		<br>
	</div>

	<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
	<script src="https://momentjs.com/downloads/moment.min.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.1/Chart.min.js"></script>

	<script>
		var canvas = document.getElementById('myChart');
		var ctx = canvas.getContext('2d');

		var data = JSON.parse(canvas.getAttribute('temps'));
		var labels = JSON.parse(canvas.getAttribute('times'));
		var points = [];

		for (var i = 0; i < data.length; i++) {
			points.push({t:new Date(labels[i]),y:data[i]});
		}

		var myChart = new Chart(ctx, {
			type: 'line',
			data: {
				labels: labels,
				datasets: [{
					label: 'Temperature in degrees Celcius',
					data: points,
					backgroundColor: 'rgba(80, 40, 20, 0.2)',
					borderColor: 'rgba(255,0,0,1)',
					borderWidth: 2,
				}],
			},
			options: {
				scales: {
					yAxes: [{
						ticks: {
							beginAtZero:true
						}
					}],
					xAxes: [{
						type: 'time',
						distribution: 'linear',
						time: {
							displayFormats: {
								hour: 'HH',
								minute: 'HH:mm',
								second: 'HH:mm:SS',
								day: 'D/M/\'YY',
								month: 'M/\'YY',
								year: '\'YY'
							}
						}
					}],
					responsive: true,
					maintainAspectRatio: true
				},
				tooltips: {
					callbacks: {
						title: function(arr, data) {
							return 'Temperature at ' + moment(data['labels'][arr[0]['index']]).format('HH:mm \o\\n DD/MM/\'YY');
						}
					}
				}
			}
		});
	</script>
</body>
</html>
