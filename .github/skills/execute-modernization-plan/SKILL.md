---
name: execute-modernization-plan
description: Execute the modernization plan by running the tasks listed in the plan
---

# Execute modernization plan

This skill is used to execute a modernization plan to migrate the a given project to Azure

# User Input

run-modernization-requirement: The user intent to run the modernization plan
modernization-folder (Mandatory): The folder to save the modernization plan
programming-language: Input by user or autodetect by context

You **MUST** consider the user input before proceeding.

## Workflow

Given that modernization description, do this:

1. According to the run-modernization-requirement, copy the tasks in scope in the ${modernization-folder}/plan.md into the ${modernization-folder}/modernization-progress.md and loop each task in the modernization-progress.md and call the custom agent to execute the task.

    - You must track the tasks in modernization-progress.md. The following is a sample of what you should provide in modernization-progress.md and track in modernization-progress.md.
        - **Task Type**": One of JavaUpgrade, MigrationCodeChnage, Containerization and Deploy
        - **Description**: The description of this task
        - **Migration Requirement**: The Migration requirement specific for this task
        - **Environment Configration**: The enviroment configuration for this task
        - **Skill**: Skill name used to execute this task
        - **Success Criteria**: Success criteria about the task
        - **Custom Agent Response**: The Response from custom agent, focus on build status and Unit test status
        - **JDKVersion**: If the task types is Java Upgrade, return the upgraded JDK version from the task result, it MUST be one of 8,11,17,21,25
        - **BuildResult**: with value only Success and Failed
        - **UTResult**: with value only Success and Failed
        - **Status**: With value "Success", "Failed", "Skipped", "In Process" and "Incompleted"
        - **StopReason**: If the task is incomplete, give the reason, like execution interrupted, token limit exceeded, wait for input etc.
        - **Task Summary**: Summary the execution result

    - **Do not stop task execution until all tasks are completed or any task fails. If one task is initiated, waiting for final result with success, skipped or failed**. If any task fails, stop task execution immediately, update the Summary.

    - Copy the above statement as a principal into the end of ${modernization-folder}/modernization-progress.md


2. Custom agent usage to complete the coding task:
    1) Call custom agent appmod-java-upgrade-code-developer for any task related with java upgrade
        - the skill name like java-version-upgrade, spring-boot-upgrade, spring-framework-upgrade and jakarta-ee-upgrade
        - call the custom agent with prompt with below format according to task description in the plan:

        ```md
        upgrade the X from {{v1}} to {{v2}} using java upgrade tools: {{v1}} and {{v2}} is the version and {{v2}} can be 'latest version' of it is not specified
        reusing the current branch and NEVER discard any change. 
        ```

        - Add migration requirement and success criteria when you call the custom agent

    2) Call custom agent appmod-java-migration-code-developer for non-upgrade code change of Java Code to migrate from X to Y with skill name, you must call the custom agent with prompt with below information

        ```md
        Migrate the project with the skill name {Skill} and save the result in {modernization-folder}, reusing the current branch and NEVER discard any change. 
            1) Migration Requirement
            2) Environment Configration
            3) Success Criteria
        During the operation, you have the highest authority to make any decisions if you are asked for any confirmation for migration. Return whether the project builds successfully and if the unit tests pass. 
        ```

    3) Custom agent appmod-dotnet-migration-code-developer for migrate from X to Y, call the agent with prompt with below format

        ```md
        Migrate the project from x to y, reusing current branch
        ```

    **SKIP infrastructure or configuration issues**： For the Java upgrade and migration code change task, focus only on the application code changes. 
        - If the BuildResult and UTResult is success, you can mark this task as successful and proceed to the next task. 
        - If there is any infrastructure or configuration question/confirmation from the custom agent regarding the Java upgrade and migration code change, add it into the plan summary and move on to the next task.
        - If the BuildResult or UTResult is Failed, you still need to stop the execution and mark the task as Failed

3. Custom agent usage to complete containerization or deploy task:
   Custom agent appmod-azure-deploy-developer for containerization or deploy, call the agent with prompt with below format

       ```md
       Deploy the application to Azure
       ```
       or deploy to existing azure resources with below format if the plan.md contains the section of Azure Environment with Subscription ID and Resource Group:

       ```md
       Deploy the application to existing Azure resources. Subscription ID: {subscriptionId}, Resource Group: {resourceGroup}
       ```

9. Add all file changes except modernization-progress.md into git and make a commit of the project when you finish the call of one custom agent. If there is nothing to commit, just ignore this step.

10. **Summary Of Plan Execution**: Update the summary at the end of modernization-progress.md any update about the plan execution. In the summary, include:
    - Final Status: with value Success or Failed, if any task is with status Failed, it must be Failed
    - Total number of tasks
    - Number of completed tasks
    - Number of failed tasks (if any)
    - Number of cancelled tasks (if any)
    - Overall status (e.g., "Plan execution completed successfully" or "Plan execution completed with errors")
    - A brief summary of what was accomplished
    - Plan Execution Start Time
    - Plan Execution End Time
    - Total Minutes for Plan Execution
