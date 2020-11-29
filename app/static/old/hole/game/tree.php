<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"/>
    <title>Eglite</title>
    <style type="text/css">
        body{
            margin:0;
            padding:0;
            color:#000;
            background:#efefef url('') repeat center top;
            font:normal 0.9em/150% 'Arimo', "Trebuchet MS", arial, verdana, sans-serif;
            text-shadow: 0px 0px 1px transparent;
        }
        #container{
            width:960px;
            min-height: 300px;
            background:#FFFFFF;
            margin:30px auto 30px auto;
            padding:0;
            border:1px solid #ccc;
        }
        .result, .rules{
            text-align: center;
            font-size: 18px;
            -webkit-perspective:800;
        }
        input[type="submit"]{
            background-color: #82B900;
            width: 90px;
            height: 40px;
            border-radius: 5px;
            margin: 20px 420px;
            border: 1px solid #008000;
            font-family: "Trebuchet Ms", arial, verdana, sans-serif;
            color: #FFFFFF;

        }
        b{
            color: #339966;
        }
        .egle{
            color:#339966;
            font-size: 14px;
            transform:rotate(30deg);
            width: 400px;
            margin:0 auto;
            text-shadow:5px 5px 10px black;
        }
        .egle b{
            font-size: 17px;
        }
        .egle:hover{
            font-size: 15px;
            -webkit-transition:all 1s linear;
            /*-webkit-box-shadow: 0px 0px 50px #000;*/
            /* border-radius: 25px;*/
            /*background: #DEFBFA;*/
            text-shadow:5px 5px 10px black;
            /* -webkit-transform: rotate3d(100,100,100,10deg);*/
            /*-webkit-transform: rotateZ(90deg);*/

        }
        .game{
            color: white;
            background: #3366FF;
            text-decoration: none;
            width: 70px;
            height: 30px;
            display:block;
            text-align: center;
            border-radius: 20px;
        }
        .game:hover{
            -webkit-transition:all 1s linear;
            /*-webkit-transform: rotate3d(100,100,100,360deg);*/
            text-shadow:5px 5px 10px black;
            box-shadow:2px 2px 2px 2px black;
        }
    </style>

</head>
<body>
<div id="container">
    <div class="rules">
        <a class="game" href="index.php">Back</a>
        <h1>Creating a Christmas Tree</h1>
        <p>
            Enter a number from 1-15 and this program will create a Christmas Tree.
        </p>
    </div>
    <div class="result">
        <form action="tree.php" method="post">
            <input class="section_number" type="text" name="number" maxlength="2" pattern= "[0-9]{1,2}" autocomplete="off" title="use only numbers" />
            <input type="submit" value="Create"/>
        </form>
        <div class="egle">
            <?php
            function gen($length){
                $chars = '10';
                $numChars = strlen($chars);
                $string = '';
                for ($i = 0; $i < $length; $i++) {
                    $string .= substr($chars, rand(1, $numChars) - 1, 1);
                }
                return $string;
            }

            if(isset($_POST['number']))
            {
                $hvoja = '<b> * </b>';
                $num = $_POST['number'];
                if($num == 0)
                {
                    echo '<b style="color:red;">Number is too small! The minimum is 1!</b>';
                }
                elseif($num > 0 && $num <16)
                {
                    for($y=0,$z=-1;$y<$num;$y++,$z=$z+2)
                    {
                        if($y == 0)
                        {
                            echo $hvoja.'<br />'.
                                $hvoja.gen(1).$hvoja.'<br />'.
                                $hvoja.gen(3).$hvoja.'<br />';
                        }
                        else
                        {
                            echo $hvoja.gen($z).$hvoja.'<br />'.
                                $hvoja.gen($z+2).$hvoja.'<br />'.
                                $hvoja.gen($z+4).$hvoja.'<br />';
                        }

                    }
                    if($num == 1)echo '<b style="color:#6D4F03;">*</b><br />';
                    elseif($num > 1 && $num < 5)echo '<b style="color:#6D4F03;">***</b><br />';
                    else echo '<b style="color:#6D4F03;">*****</b><br />';
                    //if($num>1)echo '<b style="color:#6D4F03;">'.gen(1*$num).'</b><br />';
                }
                else
                {
                    echo '<b style="color:red;">Number is too big! The maximum is 15!</b>';
                }
            }
            ?>
        </div>
    </div>
</div>
</body>
</html>