<?php

class ApiHandlerDiscord
{
    public function handleFormSubmission()
    {
        // Read JSON data from the request
        $jsonData = file_get_contents('php://input');
        $data = json_decode($jsonData, true);
        // Check if the JSON file contains job offer and CV data
        if (isset($data['job_offer']) && isset($data['cv'])) {
            // Extract job offer and CV data
            $jobOffer = $data['job_offer'];
            echo $job_offer . '<br>';
            $cv = $data['cv'];
            echo $cv;
            $prompt1 = "prompt_job.txt";
            $prompt2 = "prompt_cv.txt";
            $prompt3 = "prompt_match.txt";
            $prompt4 = "prompt_missing.txt";
            $promptjob = trim(file_get_contents($prompt1));
            $promptcv = trim(file_get_contents($prompt2));
            $promptmatch = trim(file_get_contents($prompt3));
            $promptmissing = trim(file_get_contents($prompt4));
            // Define the data for the API call for the job offer
            $dataJobOffer = [
                'messages' => [
                    [
                        'role' => 'system',
                        'content' => $promptjob,
                    ],
                    [
                        'role' => 'user',
                        'content' => $jobOffer,
                    ],
                ],
                'temperature' => 0,
                'max_tokens' => 3000,
                'model' => 'gpt-4',
            ];

            // Make the API call for the job offer
            $responseJobOffer = $this->callOpenAiApi($dataJobOffer);

            // Define the data for the API call for the CV
            $dataCv = [
                'messages' => [
                    [
                        'role' => 'system',
                        'content' => $promptcv,
                    ],
                    [
                        'role' => 'user',
                        'content' => $cv,
                    ],
                ],
                'temperature' => 0,
                'max_tokens' => 3000,
                'model' => 'gpt-4',
            ];

            // Make the API call for the CV
            $responseCv = $this->callOpenAiApi($dataCv);

            // Define the data for the API call to compare job offer and CV responses
            $dataMatchSkills = [
                'messages' => [
                    [
                        'role' => 'system',
                        'content' => $promptmatch,
                    ],
                    [
                        'role' => 'user',
                        'content' => $responseJobOffer['choices'][0]['message']['content'],
                    ],
                    [
                        'role' => 'system',
                        'content' => 'CV',
                    ],
                    [
                        'role' => 'user',
                        'content' => $responseCv['choices'][0]['message']['content'],
                    ],
                ],
                'temperature' => 0,
                'max_tokens' => 3000,
                'model' => 'gpt-4',
            ];

            // Make the API call to compare job offer and CV responses for matching skills
            $responseMatchSkills = $this->callOpenAiApi($dataMatchSkills);

            // Define the data for the API call to find missing skills
            $dataMissingSkills = [
                'messages' => [
                    [
                        'role' => 'system',
                        'content' => $promptmissing,
                    ],
                    [
                        'role' => 'user',
                        'content' => $responseJobOffer['choices'][0]['message']['content'],
                    ],
                    [
                        'role' => 'system',
                        'content' => 'matching skills',
                    ],
                    [
                        'role' => 'user',
                        'content' => $responseMatchSkills['choices'][0]['message']['content'],
                    ],
                ],
                'temperature' => 0,
                'max_tokens' => 3000,
                'model' => 'gpt-4',
            ];

            // Make the API call to find missing skills
            $responseMissingSkills = $this->callOpenAiApi($dataMissingSkills);

            // Prepare the result data
            $result = [
                'job_offer_result' => $responseJobOffer['choices'][0]['message']['content'],
                'cv_result' => $responseCv['choices'][0]['message']['content'],
                'matching_skills' => $responseMatchSkills['choices'][0]['message']['content'],
                'missing_skills' => $responseMissingSkills['choices'][0]['message']['content'],
            ];

            // Convert the result to JSON
            $resultJson = json_encode($result, JSON_PRETTY_PRINT);

            // Save the result as a JSON file
            file_put_contents('output.json', $resultJson);

            // Return the result JSON
            echo $resultJson;
        } else {
            // Handle the case where job offer or CV data is missing
            $error = [
                'status' => 'error',
                'message' => 'JSON file does not contain job offer or CV data.',
            ];

            // Convert the error to JSON
            $errorJson = json_encode($error, JSON_PRETTY_PRINT);

            // Return the error JSON
            echo $errorJson;
        }
    }

    // Function to make the API call using cURL
    private function callOpenAiApi($data)
    {
        $file = "Code/api.txt";
        $api_key = trim(file_get_contents($file));
        $url = 'https://api.openai.com/v1/chat/completions';
        $headers = [
            'Content-Type: application/json',
            'Authorization: Bearer ' . $api_key,
        ];

        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

        $response = curl_exec($ch);
        if ($response === false) {
            // Display cURL error if any
            echo 'cURL error: ' . curl_error($ch);
        }
        curl_close($ch);

        return json_decode($response, true);
    }
}

// Create an instance of the ApiHandler class
$apiHandlerDiscord = new ApiHandlerDiscord();

// Handle the form submission
$apiHandlerDiscord->handleFormSubmission();
