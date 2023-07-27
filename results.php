<?php
// results.php will display the results using data stored in the session.

session_start();

if (isset($_SESSION['job_offer']) && isset($_SESSION['cv']) && isset($_SESSION['matching_skills'])) {
    $job_offer = $_SESSION['job_offer'];
    $cv = $_SESSION['cv'];
    $matching_skills = $_SESSION['matching_skills'];
	$match = $_SESSION['match'];
	
                  
?>

<!DOCTYPE html>
<html>
<head>
<title>Vaardigheden uit vacaturetekst filteren - Results</title>
<link rel="stylesheet" type="text/css" href="stylesheet.css">
</head>
<body>
<button onclick="goBack()">Terug naar startpagina</button>
<h2>Uitkomst</h2>
<p>Percentage: <?php echo $match; ?></p>
    <div class="flex-container">

        <!-- Display variable 1: Required skills and tools from the job offer -->
        <div class="flex-item">
            <h3>Gevraagde vaardigheden:</h3>
            <p><?php echo nl2br($job_offer); ?></p>
        </div>

        <!-- Display variable 2: Skills and tools from the candidate's CV -->
        <div class="flex-item">
            <h3>Jouw vaardigheden:</h3>
            <p><?php echo nl2br($cv); ?></p>
        </div>

        <!-- Display variable 3: Matching skills and tools -->
        <div class="flex-item">
            <h3>Overeenkomende vaardigheden:</h3>
            <p><?php echo nl2br($matching_skills); ?></p>
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
