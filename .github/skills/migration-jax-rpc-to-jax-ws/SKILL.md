---
name: migration-jax-rpc-to-jax-ws
description: Migrate from JAX-RPC to JAX-WS for web services. JAX-RPC is deprecated and JAX-WS is the recommended alternative.
---

# jax-rpc-to-jax-ws

## Overview

Migrate from JAX-RPC to JAX-WS for web services. JAX-RPC is deprecated and JAX-WS is the recommended alternative.

## Knowledge Base Content

* KB ID: jax-rpc-to-jax-ws
* Title: Migrate JAX-RPC to JAX-WS
* Description: Provides specifications for migrating from JAX-RPC to JAX-WS
* Content: 
Migrate JAX-RPC to JAX-WS for current project. Requirements:
 - When modify files, double check whether it's necessary, don't do unnecessary change. For example
   - Don't add new business logic.
   - Don't delete existing business logic.
   - Don't upgrade dependency's version if original version can still work.
 - When adding new dependencies, double check the version is compatible with existing java version and tomcat version.
 - When updating web.xml, double check it's compatible with existing tomcat version.
 - Delete unused files. Example: JAX-RPC configuration files.
