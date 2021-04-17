<?php
require "vendor/autoload.php";

if(!empty($_POST['latitude']) && !empty($_POST['longitude'])){
    // Send request and receive json data by latitude and longitude
     $url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='.trim($_POST['latitude']).','.trim($_POST['longitude']).'&sensor=false';
    // $url = "https://www.google.co.in/maps/search/12.901000,+80.128333/";
    $json = @file_get_contents($url);
    $data = json_decode($json);
    $status = $data->status;
    if($status=="OK"){
        //Get address from json data
        $location = $data->results[0]->formatted_address;
    }else{
        $location =  'Driver Last seen Location   ';
    }
    // dipslay address
    echo $location;
    echo $_POST['latitude'];
    echo " , ";
    echo $_POST['longitude'];
	echo " &nbsp";
    $geocoder = new \OpenCage\Geocoder\Geocoder('f03bc05844dc49ddbab30099637e0b76');
$result = $geocoder->geocode('12.848334277912778, 80.1953923241745');
$result1 = $geocoder->geocode("{$_POST['latitude']}  {,}  {$_POST['longitude']} "); # latitude,longitude (y,x)
print $result['results'][0]['formatted'];
}

?>
<?php
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\SMTP;
use PHPMailer\PHPMailer\Exception;


// Load Composer's autoloader
require 'vendor/autoload.php';

// Instantiation and passing `true` enables exceptions
$mail = new PHPMailer(true);

try {
    //Server settings
//    $mail->SMTPDebug = SMTP::DEBUG_SERVER;                      // Enable verbose debug output
    $mail->isSMTP();                                            // Send using SMTP
    $mail->Host       = 'smtp.gmail.com';                    // Set the SMTP server to send through
    $mail->SMTPAuth   = true;                                   // Enable SMTP authentication
    $mail->Username   = 'mrinalmahindran@gmail.com';                     // SMTP username
    $mail->Password   = 'Suvasam123';                               // SMTP password
    $mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;         // Enable TLS encryption; `PHPMailer::ENCRYPTION_SMTPS` encouraged
    $mail->Port       = 587;                                    // TCP port to connect to, use 465 for `PHPMailer::ENCRYPTION_SMTPS` above

    //Recipients
    $mail->setFrom('mrinalmahindran@gmail.com', 'admin');
    $mail->addAddress('eagalaivanram@gmail.com ', 'User');     // Add a recipient
    // Name is optional
    // $mail->addReplyTo('info@example.com', 'Information');
    // $mail->addCC('cc@example.com');
    // $mail->addBCC('bcc@example.com');

    // // Attachments
    // $mail->addAttachment('/var/tmp/file.tar.gz');         // Add attachments
    // $mail->addAttachment('/tmp/image.jpg', 'new.jpg');    // Optional name

    // Content
    $mail->isHTML(true);                                  // Set email format to HTML
    $mail->Subject = 'Driver Location';
    $mail->Body    = "{$_POST['latitude']}  {$result['results'][0]['formatted']}   {$_POST['longitude']} ";
    $mail->AltBody = 'This is the body in plain text for non-HTML mail clients';

    $mail->send();
    echo 'Message has been sent';
} catch (Exception $e) {
    echo "Message could not be sent. Mailer Error: {$mail->ErrorInfo}";
}


?>