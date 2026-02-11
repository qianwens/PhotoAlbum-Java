---
name: create-modernization-plan
description: Create a modernization plan to migrate the project to Azure
---

# Create modernization plan

This skill is used to create a modernization plan to migrate the a given project to Azure

## User Input

modernization-requirement: The user input to generate the modernization plan
modernization-folder (Mandatory): The folder to save the modernization plan
github-issue-link (Optional): A github issue to track the modernization status
assessment-report (Optional): A assessment report for the project will be modernized, it will provide the data about the project for modernization

## Workflow

Given the user input, do this:

1. Double Check the issues
   **IMPORTANT**:
   - If you are given an assessment-report, you need to double check if the issue really exist in current project. If not, please ignore this issue when you generate the plan 

2. **Load context**: Retrieve information for plan, you can read
    1) Analysis the agent skills to find the right skill for the issues
    2) Analysis modernization requirement from user input

3. **Generate plan**: Generate plan.md using plan-template.md, you will read
    1) Follow the structure of the plan-template.md to generate the plan, use the skill start with migration or modernization to break the task
    2) Follow the rules defined in the template to fill in the sections with relevant information based on the analysis of user input and content of mentioned files
    3) Save the plan in folder ${modernization-folder} with the filename plan.md. If a plan already exists, overwrite it.

4. **Clarification**: If there are any open issues in the plan
    1) Return all the open issues to user for clarification
    2) After user clarified, update the plan

## Completion Criteria

1. All the open issues are clarified and the plan is updated
2. The modernization task list is built
3. The modernization task list MUST be scoped according to user input
4. DON'T RUN the plan if user does not explicitly ask you to run the plan