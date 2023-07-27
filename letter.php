<?php
// letter.php will display the motivation letter.

session_start();

if (isset($_SESSION['motivation'])) {
    
	$letter = $_SESSION['motivation'];
	
                  
?>

<!DOCTYPE html>
<html>
<head>
<title>Motivatiebrief</title>
<link rel="stylesheet" type="text/css" href="stylesheet.css">
</head>
<body>
<button onclick="goBack()">Terug naar startpagina</button>
<h2>Motivatiebrief</h2>

    <div class="flex-container">

        <!-- Display variable 1: Required skills and tools from the job offer -->
        <div class="flex-item">
            
            <p><?php echo nl2br($letter); ?></p>
        </div>

       
    </div>
	
<script>
        // JavaScript function to go back to index.php
        function goBack() {
            window.location.href = 'index.php';
        }
    </script>	
</body>
</html>

<?php

} else {
    // If session data is not available, redirect back to the index page
    header("Location: index.php");
    exit();
}
?>
