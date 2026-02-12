# Upgrade Plan

## Overview
Upgrade Java application to the latest LTS versions: Java 21 and Spring Boot 3.4.

## Objectives
- Migrate to Java 21 (Long Term Support)
- Upgrade Spring Boot to version 3.4
- Ensure all dependencies are compatible with target versions
- Migrate from javax.* to jakarta.* namespace where applicable

## Tasks
See `tasks.json` for detailed task breakdown and execution order.

## Target Versions
- **Java**: 21 (LTS)
- **Spring Boot**: 3.4
- **Spring Framework**: 6.x

## Prerequisites
- Backup current project state
- Review breaking changes in Java 21 and Spring Boot 3.x documentation
- Verify third-party dependency compatibility
