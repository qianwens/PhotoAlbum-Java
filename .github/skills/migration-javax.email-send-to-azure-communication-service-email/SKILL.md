---
name: migration-javax.email-send-to-azure-communication-service-email
description: Migrate from Javax Email to Azure Communication Service for sending emails.
---

# javax.email-send-to-azure-communication-service-email

## Overview

Migrate from Javax Email to Azure Communication Service for sending emails.

## Knowledge Base Content

* KB ID: microsoft://email-tasks/javax.email-send-to-azure-communication-service-email/mail-exception.formula
* Title: Migrate java mail exceptions to Azure Communication Service email exceptions
* Description: Migrate java mail exceptions to Azure Communication Service email exceptions
* Content: 
### Search code
Search files from workspace using below patterns:
- Glob pattern to find files: `**/*.java`
- Regex pattern to find code lines: `/MessagingException|AuthenticationFailedException|FolderClosedException|FolderNotFoundException|IllegalWriteException|MailConnectException|MessageRemovedException|MethodNotSupportedException|NoSuchProviderException|ParseException|ReadOnlyFolderException|SearchException|SendFailedException|SMTPAddressSucceededException|StoreClosedException|(\s)MailException|MailAuthenticationException|MailParseException|MailPreparationException|MailSendException|MailValidationException|MailCompletenessException|MailInvalidAddressException|MailSuspiciousCRLFValueException|(\s)EmailException/`
> you could use tools to search code whatever if possible.
### Instruction

Your task is to remove all exceptions from Java Mail (javax.mail.*), Spring Java Mail (org.springframework.mail.*), Simple Java Mail (org.simplejavamail.*) and Apache Commons Email (org.apache.commons.mail.*), use `EmailSendResult` and `EmailSendStatus` from Azure Communication Service email to handle them.
Below is a reference to the relevant APIs for your convenience. You can tell whether it's JavaMail or Azure API from the package name.
Some of the methods are of the same name under different class, please pay attention to the type before using.

Class: MessagingException extends Exception
  Description: The base class for all exceptions thrown by the Messaging classes.
  Package: javax.mail
  Methods:
    - public Exception getNextException()
      Description: Get the next exception chained to this one. If the next exception is a MessagingException, the chain may extend further.
      Returns: next Exception, null if none.
    - public Throwable getCause()
      Description: Overrides the getCause method of Throwable to return the next exception in the chain of nested exceptions.
      Returns: next Exception, null if none.
    - public boolean setNextException(Exception ex)
      Description: Add an exception to the end of the chain. If the end is not a MessagingException, this exception cannot be added to the end.
      Parameters:
        - ex - the new end of the Exception chain
      Returns: true if this Exception was added, false otherwise.

Class: AuthenticationFailedException extends MessagingException
  Description: This exception is thrown when the connect method on a Store or Transport object fails due to an authentication failure (e.g., bad user name or password).
  Package: javax.mail

Class: FolderClosedException extends MessagingException
  Description: This exception is thrown when a method is invoked on a Messaging object and the Folder that owns that object has died due to some reason.
  Package: javax.mail

Class: FolderNotFoundException extends MessagingException
  Description: This exception is thrown by Folder methods, when those methods are invoked on a non existent folder.
  Package: javax.mail

Class: IllegalWriteException extends MessagingException
  Description: The exception thrown when a write is attempted on a read-only attribute of any Messaging object.
  Package: javax.mail

Class: MailConnectException extends MessagingException
  Description: A MessagingException that indicates a socket connection attempt failed. Unlike java.net.ConnectException, it includes details of what we were trying to connect to. The underlying exception is available as the "cause" of this exception.
  Package: com.sun.mail.util

Class: MessageRemovedException extends MessagingException
  Description: The exception thrown when an invalid method is invoked on an expunged Message. The only valid methods on an expunged Message are isExpunged() and getMessageNumber().
  Package: javax.mail

Class: MethodNotSupportedException extends MessagingException
  Description: The exception thrown when a method is not supported by the implementation.
  Package: javax.mail

Class: NoSuchProviderException extends MessagingException
  Description: This exception is thrown when Session attempts to instantiate a Provider that doesn't exist.
  Package: javax.mail

Class: ParseException extends MessagingException
  Description: The exception thrown due to an error in parsing RFC822 or MIME headers, including multipart bodies.
  Package: javax.mail.internet

Class: ReadOnlyFolderException extends MessagingException
  Description: This exception is thrown when an attempt is made to open a folder read-write access when the folder is marked read-only.
  Package: javax.mail

Class: SearchException extends MessagingException
  Description: The exception thrown when a Search expression could not be handled.
  Package: javax.mail.search

Class: SendFailedException extends MessagingException
  Description: This exception is thrown when the message cannot be sent.
  Package: javax.mail

Class: SMTPAddressSucceededException extends MessagingException
  Description: This exception is chained off a SendFailedException when the mail.smtp.reportsuccess property is true. It indicates an address to which the message was sent. The command will be an SMTP RCPT command and the return code will be the return code from that command.
  Package: com.sun.mail.util

Class: StoreClosedException extends MessagingException
  Description: This exception is thrown when a method is invoked on a Messaging object and the Store that owns that object has died due to some reason. This exception should be treated as a fatal error; in particular any messaging object belonging to that Store must be considered invalid.
  Package: javax.mail

Class: MailException extends NestedRuntimeException
  Description: Base class for all mail exceptions.
  Package: org.springframework.mail

Class: MailAuthenticationException extends MailException
  Description: Exception thrown on failed authentication.
  Package: org.springframework.mail

Class: MailParseException extends MailException
  Description: Exception thrown if illegal message properties are encountered.
  Package: org.springframework.mail

Class: MailPreparationException extends MailException
  Description: Exception to be thrown by user code if a mail cannot be prepared properly, for example when a FreeMarker template cannot be rendered for the mail text.
  Package: org.springframework.mail

Class: MailSendException extends MailException
  Description: Exception thrown when a mail sending error is encountered. Can register failed messages with their exceptions.
  Package: org.springframework.mail

Class: MailValidationException extends org.simplejavamail.MailException
  Package: org.simplejavamail.mailer

Class: MailCompletenessException extends MailValidationException
  Package: org.simplejavamail.mailer
  
Class: MailInvalidAddressException extends MailValidationException
  Package: org.simplejavamail.mailer

Class: MailSuspiciousCRLFValueException extends MailValidationException
  Package: org.simplejavamail.mailer

Class: EmailException extends Exception
  Description: Exception thrown when a checked error occurs in commons-email.
  Package: org.apache.commons.mail2.core

Class: EmailSendResult
  Description: Status of the long running operation.
  Package: com.azure.communication.email.models
  Methods:
    - public ResponseError getError()
      Description: Get the error property: Response error when status is a non-success terminal state.
      Returns: the error value.
    - public String getId()
      Description: Get the id property: The unique id of the operation. Use a UUID.
      Returns: the id value.
    - public EmailSendStatus getStatus()
      Description: Get the status property: Status of operation.
      Returns: the status value.

Class: EmailSendStatus
  Description: Status of operation.
  Package: com.azure.communication.email.models
  Fields:
    - public static final EmailSendStatus CANCELED
      Description: Static value Canceled for EmailSendStatus.
    - public static final EmailSendStatus FAILED
      Description: Static value FAILED for EmailSendStatus.
    - public static final EmailSendStatus NOT_STARTED
      Description: Static value NotStarted for EmailSendStatus.
    - public static final EmailSendStatus RUNNING
      Description: Static value Running for EmailSendStatus.
    - public static final EmailSendStatus SUCCEEDED
      Description: Static value Succeeded for EmailSendStatus.
