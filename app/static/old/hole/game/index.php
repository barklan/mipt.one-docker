<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <title>Adapt</title>
    <style type="text/css">
        .num{
            font-size: 244px;
            height: 270px;
            margin: 0 auto;
            text-align: center;
            width: 318px;
        }
        input[value="Guess"]{
            background-color: #82B900;
            width: 90px;
            height: 40px;
            border-radius: 5px;
            margin: 20px;
            border: 1px solid #008000;
            font-family: "Trebuchet Ms", arial, verdana, sans-serif;
            color: #FFFFFF;
        }
        input[value="Guess"]:hover{
            background-color: #99CC00;
        }
        input[value="Play Again"]{
            background-color: #00CCFF;
            color: white;
            width: 90px;
            height: 40px;
            margin: 20px;
            border-radius: 5px;
        }
        body{
            margin:0;
            padding:0;
            color:#000;
            background:#efefef url('') repeat center top;
            font:normal 0.9em/150% 'Arimo', "Trebuchet MS", arial, verdana, sans-serif;
            text-shadow: 0px 0px 1px transparent;
            -webkit-perspective:800;
        }
        #container{
            width:960px;
            height: 700px;
            background:#FFFFFF;
            margin:30px auto 30px auto;
            padding:0;
            border:1px solid #ccc;
        }
        #num{
            text-align: center;
            /*margin-left: 300px;*/
            border-radius: 7px;
        }
        .rules{
            padding: 20px;
            font-weight: bold;
        }
        .rew{
            text-align: center;
        }
        .result{
            text-align: center;
        }
        a#eglite{
            color: white;
            background: #3366FF;
            text-decoration: none;
            width: 70px;
            height: 30px;
            border-radius: 10px;
            display:block;
            text-align: center;

        }

    </style>
</head>
<body>
<div id="container">
    <div class="rules">
        <h2>Guessing Game</h2>
        <p>
            Game Rules: Computer randomly chooses a number from 0-99.
            You have 10 tries to guess the number.
            After each guess you will get a hint whether the number you have to guess is bigger or smaller than the one you pick.
        </p>
    </div>
        <div class="result">
        <?php
        session_start();
        if(!isset($_SESSION['number']))
        {
            $number = rand(0,99);
            $_SESSION['number'] = $number;
            $_SESSION['p'] = 0;
            header('Location: index.php');
        }
        else
        {
            //echo 'число: '.$_SESSION['number'].'<br />';
            //echo 'попытка: '.$_SESSION['p']."<br />";
            ?>
            <form action="index.php" method="post">
                <input id="num" class="num" type="text" size="2" value="" autocomplete="off" title="только числа" maxlength="2" pattern= "[0-9]{1,2}" name="number"/><br />
                <input id="button" type="submit" value="Guess" name="" />
            </form>
            <?php
            if(isset($_POST['number']) && ( $_SESSION['p'] < 9))
            {
                if(!empty($_POST['number']))$_SESSION['p'] ++;
                if($_POST['number'] > $_SESSION['number'])
                {
                    echo "<div class='rew'>Number you have to guess is smaller <br />Your previosly entered number: ".$_POST['number']."<br />Count of tries: ".$_SESSION['p']."</div>";
                }
                elseif($_POST['number'] < $_SESSION['number'])
                {
                    echo "<div class='rew'>Number you have to guess is bigger <br />Your previosly entered number: ".$_POST['number']."<br />Count of tries:  ".$_SESSION['p']."</div>";
                }
                else
                {
                    ?>
                    <script>
                        var name_input = document.getElementById('num');
                        name_input.value='<?=$_SESSION['number'];?>';
                        var name_button = document.getElementById('button');
                        name_button.value = 'Play Again';
                    </script>
                    <?php
                    unset($_SESSION['number']);
                    ?>
                    <?php
                }
            }
            elseif(isset($_POST['number']) && ( $_SESSION['p'] == 9))
            {
                $_SESSION['p'] ++;
                ?>
                <script>
                    var name_input = document.getElementById('num');
                    name_input.value='<?=$_SESSION['number'];?>';
                    var name_button = document.getElementById('button');
                    name_button.value = 'Play Again';
                </script>
                <?php
                unset($_SESSION['number']);
                unset($_SESSION['p']);
            }
        }
        ?>
    </div> 
</div>
</body>
</html>