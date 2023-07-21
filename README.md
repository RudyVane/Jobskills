# Skill Extraction and Comparison API

The Skill Extraction and Comparison API is designed to facilitate the extraction of skills from a job offer text and a user's skill matrix, as well as compare the extracted skills to generate a list of matching skills, a list of missing skills, and calculate the matching percentage. This API leverages ChatGPT, an advanced language model, to perform these tasks. This API will work as a Discord bot.

## Purpose

The primary purpose of this API is to provide a seamless solution for extracting and comparing skills between a job offer and a user's skill matrix. It enables the identification of skills required for a job and helps users determine which skills they possess and which skills they need to acquire.

## Skill Extraction from Job Offer Text

The API allows users to extract skills from a job offer text. By providing the job offer text as input, the API utilizes natural language processing techniques to parse the text and identify the required skills. The extracted skills are then delivered as structured output, such as a JSON object or a list.

## Skill Extraction from User's Skill Matrix

The API enables users to extract skills from their skill matrix. Users can input their skill matrix, which is a structured representation of their skills, including details like proficiency levels or years of experience. The API applies a skill extraction logic to parse the skill matrix and extract individual skills. The extracted skills are returned as output, in a format similar to the job offer skills, such as a JSON object or a list.

## Comparison of Job Offer Skills and User Skills

The API facilitates the comparison of skills between the job offer and the user's skill matrix. Users can provide both sets of skills as input to the API. Using a comparison logic, the API determines the matching skills, those skills present in both the job offer and the user's skill matrix. Additionally, the API identifies the missing skills, which are required for the job but not present in the user's skill matrix. The comparison results are delivered as output, typically in a structured format such as a JSON object or a list.

## Matching Percentage Calculation

The API includes a feature to calculate the matching percentage between the job offer skills and the user's skill matrix. By dividing the number of matched skills by the total number of job offer skills and multiplying by 100, the API determines the percentage of skills that match. This provides users with a quantitative measure of their skills' alignment with the job requirements.

## How to Use the API

To utilize the API, follow these steps:

1. Skill Extraction from Job Offer Text: Use the provided endpoint to send the job offer text as input. The API will extract the required skills and return them in a structured format, such as a JSON object or a list.

2. Skill Extraction from User's Skill Matrix: Utilize the designated endpoint to submit the user's skill matrix. The API will extract the skills from the matrix and return them in a structured format, similar to the job offer skills.

3. Comparison of Job Offer Skills and User Skills: Submit the job offer skills and the user skills to the respective endpoint. The API will compare the two sets of skills and generate the list of matching skills and missing skills. The comparison results will be returned in a structured format, such as a JSON object or a list.

4. Matching Percentage Calculation: By using the matching skills count and the total number of job offer skills, the API calculates the matching percentage. The result is provided along with the other comparison outputs.

## Conclusion

The Skill Extraction and Comparison API provides a powerful solution for extracting skills from job offer texts and user skill matrices, comparing them, and generating valuable insights. It empowers users to identify the skills they possess, determine the skills they need to acquire, and assess their skills' alignment with job requirements. By leveraging ChatGPT's language capabilities, this API offers a versatile and efficient way to streamline skill extraction and comparison processes.
The API will run as a bot on a Discordchannel. The user can communicate with the bot and provide the job offer text and user's resume. The bot returns the matched skills in the channel only visible to the user.

The first version will be a MVP, which can be expanded with more features.

The API is ment to be used by people who do or did the codeGorilla Java bootcamp or other courses at codeGorilla/Alyx

