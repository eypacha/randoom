# Randoom
Human Random Generator as a service.


## Overview

The Human Random Generator is a service that provides random numbers and words. It exposes a RESTful API built with FastAPI, allowing users to generate, save, and retrieve random values.

## API Documentation

This API adheres to the OpenAPI 3.0 specification. You can find the complete OpenAPI documentation at `/openapi.json`.

### Endpoints

#### Numbers

- **Operations with numbers**

  - **GET /random/number/**
    - Retrieve a random number.
    
  - **POST /random/number/**
    - Save a random number.

  - **GET /random/number/stats/**
    - Get statistics of the saved numbers.

#### Words

- **Operations with words**

  - **GET /random/word/**
    - Retrieve a random word.
    
  - **POST /random/word/**
    - Save a random word.

  - **GET /random/word/stats/**
    - Get statistics of the saved words.