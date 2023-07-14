# GPT-3 API Sample Code

This sample code demonstrates the usage of the OpenAI GPT-3 API to interact with the GPT-3.5-turbo model. It includes a chat function and a comparison mode that calculates the percentage of matching skills between a skills matrix and a job advert.

## Description

The code utilizes the OpenAI GPT-3 API to facilitate natural language interactions. It leverages the `chat_with_gpt3` function to have a conversation with the GPT-3 model and obtain responses. Additionally, it includes a `compare_mode_interaction` function that compares a skills matrix file and a job advert file to determine the percentage of matching skills using the GPT-3 chat functionality.

## Prerequisites

To run this code, you need an OpenAI API key, which should be stored in a `.env` file. The `.env` file should contain the API key as follows:

API_KEY=<your-api-key>