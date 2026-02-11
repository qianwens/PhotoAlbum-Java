---
name: migration-s3-to-azure-blob-storage
description: Migrate from AWS S3 to Azure Blob Storage for scalable and secure object storage in Azure.
---

# s3-to-azure-blob-storage

## Overview

Migrate from AWS S3 to Azure Blob Storage for scalable and secure object storage in Azure.

## Knowledge Base Content

* KB ID: microsoft://storage-tasks/s3-to-azure-blob-storage/s3-accessPolicy.formula
* Title: Migrate S3 Access Policy to Azure Blob SAS Token
* Description: Migrate Amazon S3 access policy logic to Azure Blob Storage using SAS token generation.
* Content: 
### Search code
Search files from workspace using below patterns:
- Glob pattern to find files: `**/*.java`
- Regex pattern to find code lines: `/PutBucketPolicyRequest|DeleteBucketPolicyRequest|GetBucketPolicyRequest|AccessControlPolicy/`
> you could use tools to search code whatever if possible.
### Instruction

Your task is to migrate code that relies on Amazon S3 access policies (which use JSON policy documents, bucket policies, or IAM-based controls) to the Azure Storage Blob model that uses Shared Access Signature (SAS) tokens.

In Amazon S3:
- Access policies are typically defined in JSON format and attached to buckets or objects.
- They specify allowed actions (e.g., s3:GetObject, s3:PutObject) and conditions under which these actions are permitted.

In Azure Storage Blob:
- SAS tokens are generated to delegate specific permissions (e.g., read, write, delete) for a given container or blob.
- These tokens are created using methods such as BlobContainerClient.generateSas() or BlobServiceClient.generateUserDelegationSas(), and include parameters like expiry time, permissions, and optionally IP restrictions.

Note:
  1. The package of `BlobClient` is com.azure.storage.blob and the package of `BlobClientBase` is com.azure.storage.blob.specialized, don't make mistake here.
  2. The package of `BlobContainerClient` is com.azure.storage.blob.BlobContainerClient, don't make mistake here.

Here are the APIs for reference, don't forget to import the package whenever you are adding a new class reference in code edit

Interface: PutBucketPolicyRequest.Builder
  Package: software.amazon.awssdk.services.s3.model
  Methods:
    - PutBucketPolicyRequest.Builder bucket​(String bucket)
      Description: The name of the bucket.
      Parameters:
        - bucket - The name of the bucket.
      Returns: Returns a reference to this object so that method calls can be chained together.
    - PutBucketPolicyRequest.Builder policy​(String policy)
      Description: The bucket policy as a JSON document.
      Parameters:
        - policy - The bucket policy as a JSON document.
      Returns: Returns a reference to this object so that method calls can be chained together.

Interface: DeleteBucketPolicyRequest.Builder
  Package: software.amazon.awssdk.services.s3.model
  Methods:
    - DeleteBucketPolicyRequest.Builder bucket​(String bucket)
      Description: The name of the bucket.
      Parameters:
        - bucket - The name of the bucket.
      Returns: Returns a reference to this object so that method calls can be chained together.

Interface: GetBucketPolicyRequest.Builder
  Package: software.amazon.awssdk.services.s3.model
  Methods:
    - GetBucketPolicyRequest.Builder bucket​(String bucket)
      Description: The name of the bucket.
      Parameters:
        - bucket - The name of the bucket.
      Returns: Returns a reference to this object so that method calls can be chained together.

Interface: AccessControlPolicy.Builder
  Package: software.amazon.awssdk.services.s3.model
  Methods:
    - AccessControlPolicy.Builder grants​(Collection<Grant> grants)
      Description: A list of grants.
      Parameters:
        - grants - A list of grants.
      Returns: Returns a reference to this object so that method calls can be chained together.
    - AccessControlPolicy.Builder grants​(Grant... grants)
      Description: A list of grants.
      Parameters:
        - grants - A list of grants.
      Returns: Returns a reference to this object so that method calls can be chained together.
    - AccessControlPolicy.Builder owner​(Owner owner)
      Description: Container for the bucket owner's display name and ID.
      Parameters:
        - owner - Container for the bucket owner's display name and ID.
      Returns: Returns a reference to this object so that method calls can be chained together.

Interface Grant.Builder
  Package: software.amazon.awssdk.services.s3.model
  Methods:
    - Grant.Builder permission​(String permission)
      Description: Specifies the permission given to the grantee.
      Parameters:
        - permission - Specifies the permission given to the grantee.
      Returns: Returns a reference to this object so that method calls can be chained together.
    - Grant.Builder grantee​(Grantee grantee)
      Description: The person being granted permissions.
      Parameters:
        - grantee - The person being granted permissions.
      Returns: Returns a reference to this object so that method calls can be chained together.
    - AccessControlPolicy.Builder owner​(Owner owner)
      Description: Container for the bucket owner's display name and ID.
      Parameters:
        - owner - Container for the bucket owner's display name and ID.
      Returns: Returns a reference to this object so that method calls can be chained together.

Class: BlobClient
  Package: com.azure.storage.blob
  Note: `The package of `BlobClient` is com.azure.storage.blob and the package of `BlobClientBase` is com.azure.storage.blob.specialized, don't make mistake here.
  Methods:
    - public String generateSas(BlobServiceSasSignatureValues blobServiceSasSignatureValues)
      Description: Generates a service SAS for the blob using the specified BlobServiceSasSignatureValues
      Parameters:
        - blobServiceSasSignatureValues - BlobServiceSasSignatureValues
      Returns: A String representing the SAS query parameters.
    - public String generateSas(BlobServiceSasSignatureValues blobServiceSasSignatureValues, Context context)
      Description: Generates a service SAS for the blob using the specified BlobServiceSasSignatureValues
      Parameters:
        - blobServiceSasSignatureValues - BlobServiceSasSignatureValues
        - context - Additional context that is passed through the code when generating a SAS.
      Returns: A String representing the SAS query parameters.
    - public String generateUserDelegationSas(BlobServiceSasSignatureValues blobServiceSasSignatureValues, UserDelegationKey userDelegationKey)
      Description: Generates a user delegation SAS for the blob using the specified BlobServiceSasSignatureValues.
      Parameters:
        - blobServiceSasSignatureValues - BlobServiceSasSignatureValues
        - userDelegationKey - A UserDelegationKey object used to sign the SAS values. See getUserDelegationKey(OffsetDateTime start, OffsetDateTime expiry) for more information on how to get a user delegation key.
      Returns: A String representing the SAS query parameters.
    - public String generateUserDelegationSas(BlobServiceSasSignatureValues blobServiceSasSignatureValues, UserDelegationKey userDelegationKey, String accountName, Context context)
      Description: Generates a user delegation SAS for the blob using the specified BlobServiceSasSignatureValues.
      Parameters:
        - blobServiceSasSignatureValues - BlobServiceSasSignatureValues
        - userDelegationKey - A UserDelegationKey object used to sign the SAS values. See getUserDelegationKey(OffsetDateTime start, OffsetDateTime expiry) for more information on how to get a user delegation key.
        - accountName - The account name.
        - context - Additional context that is passed through the code when generating a SAS.
      Returns: A String representing the SAS query parameters.

Class: BlobServiceSasSignatureValues
  Package: com.azure.storage.blob.sas
  Description: Used to initialize parameters for a Shared Access Signature (SAS) for an Azure Blob Storage service.
  Constructors:
    - BlobServiceSasSignatureValues(OffsetDateTime expiryTime, BlobSasPermission permissions)
      Description: Creates a BlobServiceSasSignatureValues object with the specified expiry time and permissions.
      Parameters:
        - expiryTime: The time after which the SAS will expire.
        - permissions: The permissions to set for the SAS.
    - BlobServiceSasSignatureValues(OffsetDateTime expiryTime, BlobContainerSasPermission  permissions)
      Description: Creates a BlobServiceSasSignatureValues object with the specified expiry time and permissions.
      Parameters:
        - expiryTime: The time after which the SAS will expire.
        - permissions - BlobContainerSasPermission allowed by the SAS.
  Methods:
    - BlobServiceSasSignatureValues setExpiryTime(OffsetDateTime expiryTime)
      Description: Sets when the SAS will expire.
      Parameters:
        - expiryTime: The time after which the SAS will expire.
      Returns: The updated BlobServiceSasSignatureValues object.
    - BlobServiceSasSignatureValues setPermissions(BlobSasPermission permissions)
      Description: Sets the permissions for the SAS.
      Parameters:
        - permissions: The permissions to set for the SAS.
      Returns: The updated BlobServiceSasSignatureValues object.

Class: BlobSasPermission
  Package: com.azure.storage.blob.sas
  Methods:
    - public BlobSasPermission setReadPermission(boolean hasAddPermission)
      Description: Sets if the permission allows for read operations.
      Parameters:
        - hasAddPermission - Permission status to set
      Returns: The updated BlobSasPermission object.
    - public BlobSasPermission setWritePermission(boolean hasAddPermission)
      Description: Sets if the permission allows for write operations.
      Parameters:
        - hasAddPermission - Permission status to set
      Returns: The updated BlobSasPermission object.
    - public BlobSasPermission setCreatePermission(boolean hasAddPermission)
      Description: Sets if the permission allows for create operations.
      Parameters:
        - hasAddPermission - Permission status to set
      Returns: The updated BlobSasPermission object.
    - public BlobSasPermission setDeletePermission(boolean hasAddPermission)
      Description: Sets if the permission allows for delete operations.
      Parameters:
        - hasAddPermission - Permission status to set
      Returns: The updated BlobSasPermission object.
    - public BlobSasPermission setAddPermission(boolean hasAddPermission)
      Description: Sets the add permission status.
      Parameters:
        - hasAddPermission - Permission status to set
      Returns: The updated BlobSasPermission object.
    - public BlobSasPermission setExecutePermission(boolean hasExecutePermission)
      Description: Sets the add permission status.
      Parameters:
        - hasAddPermission - Permission status to set
      Returns: The updated BlobSasPermission object.
    - public BlobSasPermission setListPermission(boolean hasExecutePermission)
      Description: Sets the add permission status.
      Parameters:
        - hasAddPermission - Permission status to set
      Returns: The updated BlobSasPermission object.
    - public BlobSasPermission setReadPermission(boolean hasExecutePermission)
      Description: Sets the add permission status.
      Parameters:
        - hasAddPermission - Permission status to set
      Returns: The updated BlobSasPermission object.
    - public BlobSasPermission setWritePermission(boolean hasExecutePermission)
      Description: Sets the add permission status.
      Parameters:
        - hasAddPermission - Permission status to set
      Returns: The updated BlobSasPermission object.

 Class: BlobServiceClient
  Package: com.azure.storage.blob
  Methods:
    - BlobContainerClient getBlobContainerClient(String containerName)
      Description: Gets a client pointing to the container.
      Parameters:
        - containerName: The name of the container to point to.
      Returns: A BlobContainerClient object pointing to the specified container.

Class: BlobContainerClient
  Package: com.azure.storage.blob
  Methods:
    - BlobClient getBlobClient(String blobName)
      Description: Gets a client pointing to the blob.
      Parameters:
        - blobName: The name of the blob to point to.
      Returns: A BlobClient object pointing to the specified blob.
    - public String generateSas(BlobServiceSasSignatureValues blobServiceSasSignatureValues, Context context)
      Description: Generates a service SAS for the container using the specified BlobServiceSasSignatureValues
      Parameters: 
        - blobServiceSasSignatureValues: Configurations for the service SAS.
        - userDelegationKey : Additional context that is passed through the code when generating a SAS.
      Returns: A String representing the SAS query parameters.
    - public String generateUserDelegationSas(BlobServiceSasSignatureValues blobServiceSasSignatureValues, UserDelegationKey userDelegationKey)
      Description: Generates a user delegation SAS for the container using the specified BlobServiceSasSignatureValues.
      Parameters: 
        - blobServiceSasSignatureValues: Configurations for the service SAS.
        - context: A UserDelegationKey object used to sign the SAS values. 
      Returns: A String representing the SAS query parameters.
    - public String generateSas(BlobServiceSasSignatureValues blobServiceSasSignatureValues)
      Description: Generates a service SAS for the container using the specified BlobServiceSasSignatureValues
      Parameters:
        - blobServiceSasSignatureValues: Configurations for the service SAS.
      Returns: A String representing the SAS query parameters.
    - public void setAccessPolicy(PublicAccessType accessType, List<BlobSignedIdentifier> identifiers)
      Description: Sets the container's permissions. The permissions indicate whether blobs in a container may be accessed publicly. Note that, for each signed identifier, we will truncate the start and expiry times to the nearest second to ensure the time formatting is compatible with the service. 
      Parameters:
        - accessType - Specifies how the data in this container is available to the public. See the x-ms-blob-public-access header in the Azure Docs for more information. Pass null for no public access.
        - identifiers - A list of BlobSignedIdentifier objects that specify the permissions for the container. Please see here for more information. Passing null will clear all access policies.
      Returns: N/A
    - public Response setAccessPolicyWithResponse(PublicAccessType accessType, List identifiers, BlobRequestConditions requestConditions, Duration timeout, Context context)
      Description: Sets the container's permissions. The permissions indicate whether blobs in a container may be accessed publicly. Note that, for each signed identifier, we will truncate the start and expiry times to the nearest second to ensure the time formatting is compatible with the service. 
      Parameters:
        - accessType - Specifies how the data in this container is available to the public. See the x-ms-blob-public-access header in the Azure Docs for more information. Pass null for no public access.
        - identifiers - A list of BlobSignedIdentifier objects that specify the permissions for the container. Please see here for more information. Passing null will clear all access policies.
        - requestConditions - BlobRequestConditions
        - timeout - An optional timeout value beyond which a RuntimeException will be raised.
        - context - Additional context that is passed through the Http pipeline during the service call.
      Returns: A response containing status code and HTTP headers

Class: BlobAccessPolicy
  Package: com.azure.storage.blob.models
  Description: An Access policy.
  Methods:
    - public BlobAccessPolicy setExpiresOn(OffsetDateTime expiresOn)
      Description: Set the expiresOn property: the date-time the policy expires.
      Parameters:
        - expiresOn - the expiresOn value to set.
      Returns: the BlobAccessPolicy object itself.
    - public BlobAccessPolicy setPermissions(String permissions)
      Description: Set the permissions property: the permissions for the acl policy.
      Parameters:
        - permissions - the permissions value to set.
      Returns: the BlobAccessPolicy object itself.
    - public BlobAccessPolicy setStartsOn(OffsetDateTime startsOn)
      Description: Set the startsOn property: the date-time the policy is active.
      Parameters:
        - startsOn - the startsOn value to set.
      Returns: the BlobAccessPolicy object itself.

Class: BlobSignedIdentifier
  Package: com.azure.storage.blob.models
  Description: signed identifier.
  Methods:
    - public BlobSignedIdentifier setAccessPolicy(BlobAccessPolicy accessPolicy)
      Description: Set the accessPolicy property: An Access policy.
      Parameters:
        - accessPolicy - the accessPolicy value to set.
      Returns: the BlobSignedIdentifier object itself.
    - public BlobSignedIdentifier setId(String id)
      Description: Set the id property: a unique id.
      Parameters:
        - id - the id value to set.
      Returns: the BlobSignedIdentifier object itself.
* Tags: Azure Blog Storage, Storage, AWS S3
