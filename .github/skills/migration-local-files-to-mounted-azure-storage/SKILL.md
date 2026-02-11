---
name: migration-local-files-to-mounted-azure-storage
description: Migrate from local file system to Azure Storage Account File Share mounts for scalable and secure file storage.
---

# local-files-to-mounted-azure-storage

## Overview

Migrate from local file system to Azure Storage Account File Share mounts for scalable and secure file storage.

## Knowledge Base Content

* KB ID: microsoft://storage-tasks/local-files-to-mounted-azure-storage/java.formula
* Title: Migrate to Azure Mounts - In Java file
* Description: Migrate read/write of local files to Azure Storage mounts - In Java file
* Content: 
### Search code
Search files from workspace using below patterns:
- Glob pattern to find files: `**/*.java`
- Regex pattern to find code lines: `/(?:"(([a-zA-Z]:[/\\][^"]+)|(\/(?:home|usr|Users)\/[^"]+)|(\.{1,2}[/\\][^"]+))"|:\s*(\.\.?[/\\][^}"]+))/`
> you could use tools to search code whatever if possible.
### Instruction

Your task is to migrate a Java class file from reading from or writing to hard-coded local file paths to an Azure mounted storage path while maintaining the same functionality.
1. If the code is not reading or writing files, please do nothing.
2. If the local path string is in SPEL like this: @Value("${configured.directory:../sample}"), then just change local path string to ${AZURE_MOUNT_PATH:/mnt/azure} like this: @Value("${configured.directory:${AZURE_MOUNT_PATH:/mnt/azure}}")
3. If both above 2 cases not match, the do the following things:
  3.1. Define a "private static final" field pointing to the mount path, exactly as "private static final String AZURE_MOUNT_PATH = System.getenv().getOrDefault("AZURE_MOUNT_PATH", "/mnt/azure");"
  3.2. Reference all original paths to the defined field.

For example:
From:
@Value("${configured.directory:../sample}")
To:
@Value("${configured.directory:${AZURE_MOUNT_PATH:/mnt/azure}}")

From:
private static final String INPUT_DIR = "/Users/data/csv_inputs";
To:
private static final String AZURE_MOUNT_PATH = System.getenv().getOrDefault("AZURE_MOUNT_PATH", "/mnt/azure");
private static final String INPUT_DIR = AZURE_MOUNT_PATH + "/data/csv_inputs";

From:
private static final String LOCAL_STATIC_LOCATION = "C:\\Users\\kiran\\Downloads\\imp downloads\\files\\static";
TO:
private static final String AZURE_MOUNT_PATH = System.getenv().getOrDefault("AZURE_MOUNT_PATH", "/mnt/azure");
private static final String INPUT_DIR = AZURE_MOUNT_PATH + "/files/static";

Below are some examples for your reference:
- DO NOT modify: test files
- DO NOT modify: class name, method name, field name
- DO NOT modify: commented out code
- DO modify: `File file = new File("C://some-folder/config.xml");`
- DO modify: `File file = new File("/Users/bob/config.xml");`
- DO modify: `File file = new File("/etc/config.xml");`
- DO modify: `Paths.get("C://some-folder/config.xml");`
- DO modify: `Path.of("C://some-folder/config.xml");`
- DO NOT modify: `File file = new File("/WEB-INF/config.xml");`
- DO NOT modify: `templateResolver.setPrefix("/WEB-INF/templates/");`
- DO NOT modify: `/src/main/resources`
