# LinkedIn Auto Poster

An automated bot that writes and publishes LinkedIn posts on a schedule, using AI-generated content.

## What it does

This project removes the manual work of writing and posting LinkedIn content. A scheduled GitHub Actions workflow runs the bot, which picks a topic, generates a post with an AI model, and publishes it directly to the author's LinkedIn profile.

## How it works

Topics live in topics.py, grouped into categories. The script picks a random topic from a category different than the last post's category, and skips topics already used, which are tracked in used_topics.json, so the content stays varied over time. The chosen topic is sent to Groq's Llama 3.3 70B model with a prompt describing the desired voice, tone, and structure, including a strong hook, a practical explanation, a closing takeaway, and relevant hashtags. The generated text is then published to LinkedIn through the official LinkedIn REST API. Once a post succeeds, the topic is saved to used_topics.json so it will not be repeated.

## Automation

A GitHub Actions workflow in .github/workflows triggers the script on a schedule, so new posts go out automatically without manual intervention.

## Tech stack

Python, the Groq API with the Llama 3.3 70B model for text generation, the LinkedIn REST API for publishing, and GitHub Actions for scheduling.

## Configuration

The script reads two secrets from the environment: LINKEDIN_TOKEN, a LinkedIn API access token, and GROQ_API_KEY, a Groq API key used for content generation.
