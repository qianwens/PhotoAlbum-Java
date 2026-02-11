---
name: migration-on-premises-user-authentication-to-microsoft-entra-id
description: TODO: need to further check if this aligns with the solution
---

# on-premises-user-authentication-to-microsoft-entra-id

## Overview

TODO: need to further check if this aligns with the solution

## Knowledge Base Content

* KB ID: microsoft://authentication-tasks/on-premises-user-authentication-to-microsoft-entra-id/java.formula
* Title: Update Java code for user authentication to Microsoft Entra ID authentication
* Description: Update the Java code for user authentication to Microsoft Entra ID authentication.
* Content: 
### Search code
Search files from workspace using below patterns:
- Glob pattern to find files: `**/*.java`
- Regex pattern to find code lines: `/org.springframework.security.config|SecurityConfig/`
> you could use tools to search code whatever if possible.
### Instruction

- Your task is to make the application support "login with Microsoft Entra ID" by updating this file.
- Follow these steps one by one to update this file:
    - Add "login with Microsoft Entra ID" related code by choosing one of the two options.
        - If the current configuration class extends WebSecurityConfigurerAdapter, then do the following things:
            - Change WebSecurityConfigurerAdapter to AadWebSecurityConfigurerAdapter
            - Add "http.authorizeRequests().antMatchers("/login").permitAll().anyRequest().authenticated();" in the "configure" method.
            Example:
            ```java
            import com.azure.spring.cloud.autoconfigure.aad.AadWebSecurityConfigurerAdapter;
            public static class ExampleWebSecurityConfigurerAdapter extends AadWebSecurityConfigurerAdapter {
                @Override
                protected void configure(HttpSecurity http) throws Exception {
                    super.configure(http);
                    http.authorizeRequests()
                            .antMatchers("/login").permitAll()
                            .anyRequest().authenticated();
                    // Continue with the action step described below: Merge newly added code and original code.
                }
            }
            ```
        - If the current configuration defines a SecurityFilterChain bean, then add "login with Microsoft Entra ID" related code in the bean definition method.
            - Apply AadWebApplicationHttpSecurityConfigurer by "http.with(AadWebApplicationHttpSecurityConfigurer.aadWebApplication(), Customizer.withDefaults())".
            - Add ".authorizeHttpRequests(requests -> requests.requestMatchers("/login").permitAll().anyRequest().authenticated());".
            Example:
            ```java
            import com.azure.spring.cloud.autoconfigure.implementation.aad.security.AadWebApplicationHttpSecurityConfigurer;
            public class ExampleSecurityConfig {
                @Bean
                public SecurityFilterChain htmlWebFilterChain(HttpSecurity http) throws Exception {
                    http.with(AadWebApplicationHttpSecurityConfigurer.aadWebApplication(), Customizer.withDefaults())
                        .authorizeHttpRequests(requests -> requests
                            .requestMatchers("/login").permitAll()
                            .anyRequest().authenticated());
                    return http.build();
                    // Continue with the action step described below: Merge newly added code and original code.
                }
            }
            ```
    - Merge newly added code and original code.
        - When keeping original code, make as few modifications as possible.
            - Don't change code format like indentation.
            - Don't add or delete line breaks or empty lines.
            - Don't delete code comments.
            - Don't refactor code.
        - If there is http.authorizeRequests() (or http.authorizeHttpRequests()) in original code, merge original code and newly added code. Follow these rules:
            - When using AadWebSecurityConfigurerAdapter, use http.authorizeRequests().
            - When defining a SecurityFilterChain bean, use http.authorizeHttpRequests().
            - The original http.authorizeRequests() (or http.authorizeHttpRequests()) may be inside other methods that are called by the "configure" method instead of in the "configure" method directly. Move the newly added code to the place beside original related code.
            - Merge sub methods after authorizeRequests() (or http.authorizeHttpRequests()) of original code and newly added code instead of calling authorizeRequests() (or http.authorizeHttpRequests()) twice.
            - Don't delete original business logic like "requestMatchers(...)", "antMatchers(...)" and "antMatcher(...)". CAUTION: KEEP ORIGINAL "and()" METHOD BEFORE "antMatcher(...)", LACKING THE "and()" METHOD BEFORE "antMatcher(...)" MAY CAUSE COMPILE ERRORS.
        - Keep other original HttpSecurity configuring code. Examples:
            - http.logout()
            - http.csrf()
            - http.requiresChannel()
        - Delete other HttpSecurity configuring code that conflicts with login method (login with Microsoft Entra ID). Examples:
            - Delete original authentication-related code, example: http.authenticationManager()
            - Delete original form login-related code, example: http.formLogin()
    - Delete other code that conflicts with "login with Microsoft Entra ID". Examples:
        - AuthenticationManagerBuilder configuration related code.
    - Make sure no B2C related content is added. The newly added dependency is spring-cloud-azure-starter-active-directory, not spring-cloud-azure-starter-active-directory-b2c. Don't import any B2C-related classes in Java code.
    - Refine imports.
        - Delete unused imports. Double check that they are not used anymore before deleting them. Note that "org.springframework.security.config.annotation.web.builders.HttpSecurity;" should not be deleted when it is still being used.
        - Add missing imports. Sort the newly added imports according to the existing order rule of the current file.
