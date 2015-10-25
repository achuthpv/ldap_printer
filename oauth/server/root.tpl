<html style="font-size: 30px; text-align: center;">
    <div>Access Token:</div>
    <div id="access_token"></div>
    <br><br><br>
    <div style="color: red;">Do not share this token with anyone</div>

    <script type="application/javascript">
        var access_token_div = document.getElementById('access_token');
        if (window.location.hash){
            var str = window.location.hash;
            var matches = str.match(/access_token=([^&]*)/);
            if (matches.length > 0){
                access_token_div.innerHTML = matches[1];
            }
            else{
                access_token_div.innerHTML = 'No access_token found';
            }
        }
        else{
            access_token_div.innerHTML = 'No access_token found';
        }
    </script>
</html>