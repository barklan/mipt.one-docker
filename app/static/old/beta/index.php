<!DOCTYPE html><html>
<head>

	<title>Буянов Евгений</title>
	<META content='Буянов Евгений' name="Keywords">
	<META content='Буянов Евгений' name="Description">
	<meta http-equiv="Content-Type" content="text/html; Charset=UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1.0, user-scalable=no">
	<link rel="shortcut icon" href="/favicon.ico" type="image/x-icon">
	<link rel="yandex-tableau-widget" href="/manifest.json"><meta property="og:image" content="/images/ogimage.jpg" />
	<style>
	@import url('https://fonts.googleapis.com/css?family=Abril+Fatface&display=swap');
	@import url('https://fonts.googleapis.com/css?family=Tinos&display=swap');
	html, body{padding:0; margin:0; overflow:auto;  font-family: 'Tinos', serif;}
	.b-container {display: flex; flex-direction: row; flex-wrap:wrap; font-size:0; background-image:url(/images/bg.jpg); background-size:cover; background-position:center center;}
	.b-item {width:25%; text-align:center; background:rgba(200,50,50,0.6); font-size:30vh; padding:10vh 0; line-height:100%; font-family: 'Abril Fatface', cursive; color:rgba(0,0,0,0.9);}
	.b-item:hover {background:rgba(200,50,50,0.7); color:rgba(0,0,0,1); cursor:pointer;}
	.b-item:nth-child(3n+1) {background:rgba(50,50,200,0.6)} .b-item:nth-child(3n+1):hover {background:rgba(50,50,200,0.7);}
	.b-item:nth-child(3n+2) {background:rgba(50,5200,0,0.6)} .b-item:nth-child(3n+2):hover {background:rgba(50,5200,0,0.7);}
	
	
	.b-content {position:fixed; top:0; bottom:0; width:50%; background:rgba(255,255,255,0.98); display:none; overflow:auto;}
	.b-content.left {display:block; left:0;}
	.b-content.right {display:block; right:0;}
	.b-content.center {display:block; left:25%;}
	
	.b-close-content {position:absolute; top:0; right:10px; font-size:70px; line-height:100%; color:rgba(0,0,0,0.5); cursor:pointer;}
	.b-close-content:hover { color:rgba(100,0,200,0.75);}
	
	.b-content-text {padding:20px 5%;}
	
	
	@media screen and (max-width: 800px) {
	.b-item {width:50%; font-size:9vh; padding:8vh 0;}
	
	.b-content {width:100%;}
	.b-content.left {display:block; left:0;}
	.b-content.right {display:block; right:0;}
	.b-content.center {display:block; left:0;}
	}
	</style>
</head>
<body>

<div class="b-container">
	<div class="b-item itcenter item1">B</div>
	<div class="b-item itright item2">U</div>
	<div class="b-item itleft item3">Y</div>
	<div class="b-item itcenter item4">A</div>
	<div class="b-item itcenter item5">N</div>
	<div class="b-item itright item6">O</div>
	<div class="b-item itleft item7">F</div>
	<div class="b-item itcenter item8">F</div>
</div>


<div class="b-content">
	<div class="b-close-content">×</div>
	<div class="b-content-text">Сайт Буянова Евгения</div>
</div>


<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>

<script>
$(document).ready(function(){
    $(".itcenter").click(function(){
		$(".b-content").removeClass("left");
		$(".b-content").removeClass("right");
        $(".b-content").addClass("center");
    });
	
	$(".itright").click(function(){
		$(".b-content").removeClass("left");
		$(".b-content").removeClass("center");
        $(".b-content").addClass("right");
    });

    $(".itleft").click(function(){
		$(".b-content").removeClass("center");
		$(".b-content").removeClass("right");
        $(".b-content").addClass("left");
    });	

    $(".b-close-content").click(function(){
		$(".b-content").removeClass("center");
		$(".b-content").removeClass("right");
        $(".b-content").removeClass("left");
    });	
	
	
	$(".item1").click(function(){
		$(".b-content-text").html("<h1>Давайте знакомиться</h1><p>Меня зову Евгений Буянов. Я предприматель и преподаватель.</p>");
	});	
	
	$(".item2").click(function(){
		$(".b-content-text").html("Два");
	});	
	
	$(".item3").click(function(){
		$(".b-content-text").html("Три");
	});	

	$(".item4").click(function(){
		$(".b-content-text").html("Четыре");
	});	

	$(".item5").click(function(){
		$(".b-content-text").html("Пять");
	});	

	$(".item6").click(function(){
		$(".b-content-text").html("Шесть");
	});	

	$(".item7").click(function(){
		$(".b-content-text").html("Семь");
	});	

	$(".item8").click(function(){
		$(".b-content-text").html("Восемь");
	});		
	
	
});
</script>

</body>
</html>