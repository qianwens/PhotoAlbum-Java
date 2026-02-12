---
name: execute-modernization-plan
description: Execute the modernization plan by running the tasks listed in the plan
---

# Execute modernization plan

This skill is used to execute a modernization plan to migrate the a given project to Azure

## User Input

modernization-description: The user intent to run the modernization plan
modernization-work-folder (Mandatory): The folder to save the modernization plan
programming-language: Input by user or autodetect by context

You **MUST** consider the user input before proceeding.

## Workflow

Given that modernization description, do this:
1. Read ${modernization-work-folder}/plan.md and you can have a overview with the modernization plan

2. Load all tasks from ${modernization-work-folder}/tasks.json and execute them one by one in dependency order:
    - A task can only run if all its dependent tasks (specified in the `dependencies` field) have completed successfully
    - Refer to the json schema tasks-schema.json to update the tasks.json
    - Before starting a task, update the tasks.json status to "started"
    - After completing a task, to update the tasks.json status to "success", "failed", or "skipped" with a task summary and task successCriteriaStatus
    - Do not stop task execution until all tasks are completed or any task fails. If one task is started, wait for final result with success, skipped or failed.

3. Custom agent usage to complete the coding task:
    1) You must call custom agent general-purpose for upgrade task of java with below prompt according to information from task.json, the upgrade task include java-version-upgrade, spring-boot-upgrade, spring-framework-upgrade and jakarta-ee-upgrade
        ```md
        Call skill execute-modernization-task to upgrade the X from {{v1}} to {{v2}} using java upgrade tools
        Here is the upgrade task details:
          - TaskId (from `id` field)
          - Description (from `description` field)
          - Requirements (from `requirements` field)
          - Environment Configuration (from `environmentConfiguration` field, may be null)
          - Success Criteria (from `successCriteria` field, includes: passBuild, generateNewUn
        ```
        {{v1}} and {{v2}} is the version and {{v2}} can be 'latest version' of it is not specified

    2) You must call custom agent general-purpose for transform task with below prompt according to information from task.json
        ```md
        Call skill execute-modernization-task to do the code change
        Here is the transform task details:
          - TaskId (from `id` field)
          - Description (from `description` field)
          - Requirements (from `requirements` field)
          - Migration Skills (The skill list from `skills` field used for migration)
          - Environment Configuration (from `environmentConfiguration` field, may be null)
          - Success Criteria (from `successCriteria` field, includes: passBuild, generateNewUnitTests, generateNewIntegrationTests, passUnitTests, passIntegrationTests)
          - modernization-work-folder: The folder to save the modernization plan from input      
        ```

    3) Only use the skill execute-modernization-task in custom agent to do the code change for each task
    

4. Custom agent usage to complete containerization or deploy task:
   Custom agent modernize-azure-deploy-developer for containerization or deploy, call the agent with prompt with below format
        ```md
        Deploy the application to Azure
        ```
       or deploy to existing azure resources with below format if the plan.md contains the section of Azure Environment with Subscription ID and Resource Group:
        ```md
        Deploy the application to existing Azure resources. Subscription ID: {subscriptionId}, Resource Group: {resourceGroup}
        ```

5. Output of plan execution:
   - You needn't generate any other documents except the "modernization-summary.md" for each task
   - Just make sure the tasks.json is updated with the final status of each task
   - Make a commit when all tasks are completed with the changes made in the modernization plan.
