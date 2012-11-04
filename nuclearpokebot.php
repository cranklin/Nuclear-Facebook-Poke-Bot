<?php
// your facebook credentials
$username = "email";
$password = "password";

// access to facebook home page (to get the cookies)
$curl = curl_init ();
curl_setopt ( $curl, CURLOPT_URL, "http://www.facebook.com" );
curl_setopt ( $curl, CURLOPT_FOLLOWLOCATION, 1 );
curl_setopt ( $curl, CURLOPT_RETURNTRANSFER, 1 );
curl_setopt ( $curl, CURLOPT_ENCODING, "" );
curl_setopt ( $curl, CURLOPT_COOKIEJAR, getcwd () . '/cookies.txt' );
curl_setopt ( $curl, CURLOPT_USERAGENT, "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6 (.NET CLR 3.5.30729)" );
$curlData = curl_exec ( $curl );
curl_close ( $curl );

// do get some parameters for login to facebook
$charsetTest = substr ( $curlData, strpos ( $curlData, "name=\"charset_test\"" ) );
$charsetTest = substr ( $charsetTest, strpos ( $charsetTest, "value=" ) + 7 );
$charsetTest = substr ( $charsetTest, 0, strpos ( $charsetTest, "\"" ) );

$default_persistent = 1;

$lgnjs = time();

$lgnrnd = substr($curlData, strpos($curlData, "name=\"lgnrnd\""));
$lgnrnd = substr($lgnrnd, strpos($lgnrnd, "value=")+7);
$lgnrnd = substr($lgnrnd, 0, strpos($lgnrnd,"\""));

$locale = substr ( $curlData, strpos ( $curlData, "name=\"locale\"" ) );
$locale = substr ( $locale, strpos ( $locale, "value=" ) + 7 );
$locale = substr ( $locale, 0, strpos ( $locale, "\"" ) );

$lsd = substr ( $curlData, strpos ( $curlData, "name=\"locale\"" ) );
$lsd = substr ( $lsd, strpos ( $lsd, "value=" ) + 7 );
$lsd = substr ( $lsd, 0, strpos ( $lsd, "\"" ) );

$persistent = 1;

$timezone = 480;

// login to facebook
$curl = curl_init ();
curl_setopt ( $curl, CURLOPT_URL, "https://login.facebook.com/login.php?login_attempt=1" );
curl_setopt ( $curl, CURLOPT_FOLLOWLOCATION, 1 );
curl_setopt ( $curl, CURLOPT_RETURNTRANSFER, 1 );
curl_setopt ( $curl, CURLOPT_POST, 1 );
curl_setopt ( $curl, CURLOPT_SSL_VERIFYPEER, false );
curl_setopt ( $curl, CURLOPT_POSTFIELDS, "charset_test=" . $charsetTest . "&locale=" . $locale . "&email=" . $username . "&pass=" . $password . "&lsd=" . $lsd . "&default_persistent=" . $default_persistent . "&lgnjs=" . $lgnjs . "&lgnrnd=" . $lgnrnd . "&persistent=" . $persistent . "&timezone=" . $timezone);
curl_setopt ( $curl, CURLOPT_ENCODING, "" );
curl_setopt ( $curl, CURLOPT_COOKIEFILE, getcwd () . '/cookies.txt' );
curl_setopt ( $curl, CURLOPT_COOKIEJAR, getcwd () . '/cookies.txt' );
curl_setopt ( $curl, CURLOPT_USERAGENT, "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6 (.NET CLR 3.5.30729)" );
$curlData = curl_exec ( $curl );
//echo $curlData;


// enter infinte poke loop
while(true){
    $curl = curl_init ();
    curl_setopt ( $curl, CURLOPT_URL, "https://www.facebook.com/pokes?notif_t=poke" );
    curl_setopt ( $curl, CURLOPT_FOLLOWLOCATION, 1 );
    curl_setopt ( $curl, CURLOPT_RETURNTRANSFER, 1 );
    curl_setopt ( $curl, CURLOPT_ENCODING, "" );
    curl_setopt ( $curl, CURLOPT_COOKIEFILE, getcwd () . '/cookies.txt' );
    curl_setopt ( $curl, CURLOPT_COOKIEJAR, getcwd () . '/cookies.txt' );
    curl_setopt ( $curl, CURLOPT_USERAGENT, "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6 (.NET CLR 3.5.30729)" );
    $pokeData = curl_exec ( $curl );
    //echo $pokeData;

    preg_match_all("/<div class=\"pokeHeader fsl fwb fcb\"><a href=\"(.*?)\" data-hovercard=\"\/ajax\/hovercard\/user.php\?id=([0-9]*)\">([^<]*)<\/a> has poked you.<\/div>/",$pokeData,$matches,PREG_SET_ORDER);

    if(sizeOf($matches)){
        $userid = substr ( $pokeData, strpos($pokeData, "\"user\":") + 8);
        $userid = substr ( $userid, 0, strpos($userid, "\""));

        $fb_dtsg = substr ( $pokeData, strpos ( $pokeData, "name=\"fb_dtsg\"" ) );
        $fb_dtsg = substr ( $fb_dtsg, strpos ( $fb_dtsg, "value=" ) + 7 );
        $fb_dtsg = substr ( $fb_dtsg, 0, strpos ( $fb_dtsg, "\"" ) );

        //echo $userid." ".$fb_dtsg;
        
        foreach($matches AS $val){
            //echo $val[0]."\n";
            //echo $val[1]."\n";
            //echo $val[2]."\n";
            $uid = $val[2];
            $curl = curl_init ();
            curl_setopt ( $curl, CURLOPT_URL, "https://www.facebook.com/ajax/pokes/poke_inline.php" );
            curl_setopt ( $curl, CURLOPT_FOLLOWLOCATION, 1 );
            curl_setopt ( $curl, CURLOPT_RETURNTRANSFER, 1 );
            curl_setopt ( $curl, CURLOPT_POST, 1 );
            curl_setopt ( $curl, CURLOPT_SSL_VERIFYPEER, false );
            curl_setopt ( $curl, CURLOPT_POSTFIELDS, "__a=1&nctr[_mod]=pagelet_pokes&pokeback=1&__user=" . $userid . "&fb_dtsg=" . $fb_dtsg . "&uid=" . $uid);
            curl_setopt ( $curl, CURLOPT_ENCODING, "" );
            curl_setopt ( $curl, CURLOPT_COOKIEFILE, getcwd () . '/cookies.txt' );
            curl_setopt ( $curl, CURLOPT_COOKIEJAR, getcwd () . '/cookies.txt' );
            curl_setopt ( $curl, CURLOPT_USERAGENT, "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6 (.NET CLR 3.5.30729)" );
            $pokeresults = curl_exec ( $curl );
            echo "You poked ".$val[3]."!\n";
            //echo $pokeresults;
        }
    }
    empty($matches);
    //sleep(5);
}
?>

