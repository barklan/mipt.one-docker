<!DOCTYPE HTML>
<html lang="en-US">
	<head>
		<title>Тыц</title>
		<link rel="icon" type="image/png" href="/images/mipt_logo192_2.png" sizes="192x192" />
		<meta charset="utf-8" />
		<meta name="keywords" content="KPM, jumper, КПМ, физтех, мфти, mipt">
		<meta name="viewport" content="width=device-width, initial-scale=1" />
		<link rel="stylesheet" href="/assets/css/main.css" />
		<meta http-equiv="cache-control" content="no-cache, must-revalidate, post-check=0, pre-check=0" />
		<meta http-equiv="cache-control" content="max-age=0" />
		<meta http-equiv="expires" content="0" />
		<meta http-equiv="expires" content="Tue, 01 Jan 1980 1:00:00 GMT" />
		<meta http-equiv="pragma" content="no-cache" />
	</head>
	<body>

		<script>
		window.location.href = "/hole/";
		</script>

		<div class="page-wrap">

			<!-- Main -->
				<section id="main" style="background: White !important; max-width: 1080px !important;">

					<!-- Banner -->
						<section id="banner" style="top: 50px !important;">
							<div class="inner">

								<h1>Яма v1.0</h1>

								<p>
									<?php
									$f = './download/';
									$io = popen ( '/usr/bin/du -sk ' . $f, 'r' );
									$size = fgets ( $io, 4096);
									$size = substr ( $size, 0, strpos ( $size, "\t" ) );
									pclose ( $io );
									if($size<1024){$size=$size." KB";}
									elseif(($size<1048576)&&($size>1023)){$size=round($size/1024, 1)." MB";}
									elseif(($size<1073741824)&&($size>1048575)){$size=round($size/1048576, 1)." GB";}
									else{$size=round($size/1073741824, 1)." TB";}
							    echo 'Size: ' . $size;
									?>
								</p>
								<ul class="actions">

									<!--
									<a href="https://clck.yandex.ru/redir/dtype=stred/pid=7/cid=1228/*https://yandex.ru/pogoda/214" target="_blank"><img src="https://info.weather.yandex.net/214/2_white.ru.png?domain=ru" border="0" alt="Яндекс.Погода"/><img width="1" height="1" src="https://clck.yandex.ru/click/dtype=stred/pid=7/cid=1227/*https://img.yandex.ru/i/pix.gif" alt="" border="0"/></a>
									<li><a href="https://pixlr.com/e/" class="button alt scrolly big">Pixlr</a></li>
									<li><a href="https://ocr.space/" class="button alt scrolly big">OCR</a></li>
									<li><a href="https://www.wolframalpha.com/" class="button alt scrolly big">Wolfram|Alpha</a></li>
									<li><a href="https://privatebin.net/" class="button alt scrolly big">PrivateBin</a></li>
									<li><a href="https://www.onlinegdb.com/" class="button alt scrolly big">OnlineGDB</a></li>
									<li><a href="/rickandmorty/" class="button alt scrolly big">Rick & Morty</a></li>
									-->
									<!--
									<li style="width: 100%; display: inline-block;"><p style="text-align: left; font-size: calc(7px + 1.3vw); font-family: monospace, monospace;">
										<b>5.Feb</b><i><sub>:</sub></i> | Семестр<br>
									</p></li>
									-->
									<li><a href="/download/" class="button alt scrolly big">Яма</a></li>
									<!--
									<li><a href="https://3ka.mipt.ru/stiralka" class="button alt scrolly big">Стиралка</a></li>
									-->

								</ul>
								<!--
								<img src="pool.jpg" style="object-fit: scale-down; max-width: 100%;">
								-->
							</div>
						</section>




				</section>
		</div>
		<!-- Scripts -->
			<script src="/assets/js/jquery.min.js"></script>
			<script src="/assets/js/jquery.poptrox.min.js"></script>
			<script src="/assets/js/jquery.scrolly.min.js"></script>
			<script src="/assets/js/skel.min.js"></script>
			<script src="/assets/js/util.js"></script>
			<script src="/assets/js/main.js"></script>

	</body>
</html>
