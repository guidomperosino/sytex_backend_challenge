# Sytex coding challenge 🎯

This repository holds a coding challenge for devs applying for backend jobs @ [Sytex](https://sytex.io).

## Context

In this coding challange, we will provide you with a real (albeit very diluted) business use case. The objective is that you provide a set of API for a front-end client to consume.

## The challenge!

In Sytex, a Form (think Google Forms) is used to gather information in the field. Our users would go to (sometimes *very*) remote locations to do some type of installation, improvements, upgrades or maintenance in the field. You can picture someone driving to the middle of the Atacama desert to repair a solar panel, or to a Brazilian *morro* in Rio to install a new 5G cell.

During and after the work is done, informations must be gathered, to make sure the job was done correctly, and to inform the rest of the organization about the status and results.

Forms are based on a template. The template is the set of questions (form entries) that will need to be answered in the field. For example, the questions asked to the worker repairing a solar panel would be very different that for the worker installing a brand new 5G cell.

We will provide mocked example of a couple of templates. The coding challenge consists in APIs that will allow the clients to:

- Create a new form instance, based on a given template
- Be able to answer a question with appropriate validations and sanitizations
- Get a form instance with both questions and answers included

A `FormTemplate` contains a set of entries and groups. Each `Entry` has some metadata, and an `input_type`.

Their `input_type` represents the action the user needs to do to answer ("fill") them:

**input_type:** `1`
- This is a "Text Input" `Entry`. 
- `answer` is a `String`.
- The end user would answer it using a text field.

**input_type:** `2`
- This is an "Options" `Entry`. 
- `answer` is a `String` with the value of the selected option.
- The end user would answer it using a set of radio buttons.

**input_type:** `3`
- This is a "Yes/No" `Entry`. 
- `answer` is a `boolean`.
- The end user would answer it by pressing a button with either a "Yes" or a "No" label.

## What we expect

You can go for whatever you think it's the best solution for this assignment, both code and API design! We'll check for these things in order of importance:

- API developer consumer experience.
- Whether the solution embraces standard software development patterns and practices. 

As you'll be subject to time constrains while doing this assignment, we expect you to choose what to prioritize accordingly.

## What you'll need to do

1. Clone (do not fork) the repository.
2. Understand the provided code.
3. Implement APIs to complete form's answers with corresponding validations, and provide the form data with entries and answers.
4. Upload your code to a new repository 
    - do not create a fork
    - do not create a pull request
5. [Send us the link](mailto:juan@sytex.io) to your repository with the solution
    - if you don't like the idea of your solution to be publicly available make sure to create a private repository and invite [jualvarez](https://github.com/jualvarez).
    
## Questions?

If you have any questions regarding this assignment or need to review some ideas, let us know within an issue in your repository and we'll answer promptly! Alternatively you can [send us an email](mailto:juan@sytex.io).
