<?php
if(!empty($_POST['latitude']) && !empty($_POST['longitude'])){
    //Send request and receive json data by latitude and longitude
    // $url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='.trim($_POST['latitude']).','.trim($_POST['longitude']).'&sensor=false';
    // $json = @file_get_contents($url);
    // $data = json_decode($json);
    // $status = $data->status;
    // if($status=="OK"){
    //     //Get address from json data
    //     $location = $data->results[0]->formatted_address;
    // }else{
    //     $location =  'wtf';
    // }
    // // dipslay address
    // echo $location;
    echo $_POST['latitude'];
    echo " , ";
    echo $_POST['longitude'];
}

?>