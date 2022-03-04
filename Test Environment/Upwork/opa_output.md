Running with gitlab-runner 14.4.0-rc1 (bc99a056) 

  on docker-auto-scale 0277ea0f 

  feature flags: FF_NETWORK_PER_BUILD:true 

Resolving secrets 

00:00 

Preparing the "docker+machine" executor 

01:23 

Using Docker executor with image registry.gitlab.com/infra/platform_enablement/cloud-config/cloud-config-ci-image/main ... 

Authenticating with credentials from job payload (GitLab Registry) 

Pulling docker image registry.gitlab.com/infra/platform_enablement/cloud-config/cloud-config-ci-image/main ... 

Using docker image sha256:d2d077808029d27047a3c2e761fd42bc9158f4ee0f76614c91aa6d1c2cef4601 for registry.gitlab.com/infra/platform_enablement/cloud-config/cloud-config-ci-image/main with digest registry.gitlab.com/infra/platform_enablement/cloud-config/cloud-config-ci-image/main@sha256:be853e4e5fcd965284978a37aeb05f6a68280d8592989b093cb4b250500ad823 ... 

Preparing environment 

00:03 

Running on runner-0277ea0f-project-26252347-concurrent-0 via runner-0277ea0f-srm-1634747445-342b7923... 

Getting source from Git repository 

00:03 

$ eval "$CI_PRE_CLONE_SCRIPT" 

Fetching changes with git depth set to 50... 

Initialized empty Git repository in /builds/infra/platform_enablement/cloud-config/cloud-resources/.git/ 

Created fresh repository. 

Checking out e3ed4aab as main... 

Skipping Git submodules setup 

Executing "step_script" stage of the job script 

00:05 

Using docker image sha256:d2d077808029d27047a3c2e761fd42bc9158f4ee0f76614c91aa6d1c2cef4601 for registry.gitlab.com/infra/platform_enablement/cloud-config/cloud-config-ci-image/main with digest registry.gitlab.com/infra/platform_enablement/cloud-config/cloud-config-ci-image/main@sha256:be853e4e5fcd965284978a37aeb05f6a68280d8592989b093cb4b250500ad823 ... 

$ curl --location --output artifacts.zip "https://gitlab.com/api/v4/projects/${UPSTREAM}/jobs/$UPSTREAMJOBID/artifacts?job_token=${CI_JOB_TOKEN}" -v 

* Expire in 0 ms for 6 (transfer 0x55caf3213fb0) 

* Expire in 1 ms for 1 (transfer 0x55caf3213fb0) 

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current 

                                 Dload  Upload   Total   Spent    Left  Speed 

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0* Expire in 2 ms for 1 (transfer 0x55caf3213fb0) 

* Expire in 2 ms for 1 (transfer 0x55caf3213fb0) 

* Expire in 2 ms for 1 (transfer 0x55caf3213fb0) 

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0* Expire in 2 ms for 1 (transfer 0x55caf3213fb0) 

* Expire in 2 ms for 1 (transfer 0x55caf3213fb0) 

* Expire in 2 ms for 1 (transfer 0x55caf3213fb0) 

* Expire in 2 ms for 1 (transfer 0x55caf3213fb0) 

*   Trying 172.65.251.78... 

* TCP_NODELAY set 

* Expire in 149967 ms for 3 (transfer 0x55caf3213fb0) 

* Expire in 200 ms for 4 (transfer 0x55caf3213fb0) 

* Connected to gitlab.com (172.65.251.78) port 443 (#0) 

* ALPN, offering h2 

* ALPN, offering http/1.1 

* successfully set certificate verify locations: 

*   CAfile: none 

  CApath: /etc/ssl/certs 

} [5 bytes data] 

* TLSv1.3 (OUT), TLS handshake, Client hello (1): 

} [512 bytes data] 

* TLSv1.3 (IN), TLS handshake, Server hello (2): 

{ [122 bytes data] 

* TLSv1.3 (IN), TLS handshake, Encrypted Extensions (8): 

{ [19 bytes data] 

* TLSv1.3 (IN), TLS handshake, Certificate (11): 

{ [4542 bytes data] 

* TLSv1.3 (IN), TLS handshake, CERT verify (15): 

{ [264 bytes data] 

* TLSv1.3 (IN), TLS handshake, Finished (20): 

{ [52 bytes data] 

* TLSv1.3 (OUT), TLS change cipher, Change cipher spec (1): 

} [1 bytes data] 

* TLSv1.3 (OUT), TLS handshake, Finished (20): 

} [52 bytes data] 

* SSL connection using TLSv1.3 / TLS_AES_256_GCM_SHA384 

* ALPN, server accepted to use h2 

* Server certificate: 

*  subject: CN=gitlab.com 

*  start date: Apr 12 00:00:00 2021 GMT 

*  expire date: May 11 23:59:59 2022 GMT 

*  subjectAltName: host "gitlab.com" matched cert's "gitlab.com" 

*  issuer: C=GB; ST=Greater Manchester; L=Salford; O=Sectigo Limited; CN=Sectigo RSA Domain Validation Secure Server CA 

*  SSL certificate verify ok. 

* Using HTTP2, server supports multi-use 

* Connection state changed (HTTP/2 confirmed) 

* Copying HTTP/2 data in stream buffer to connection buffer after upgrade: len=0 

} [5 bytes data] 

* Using Stream ID: 1 (easy handle 0x55caf3213fb0) 

} [5 bytes data] 

> GET /api/v4/projects/26252431/jobs/1698842521/artifacts?job_token=[MASKED] HTTP/2 

> Host: gitlab.com 

> User-Agent: curl/7.64.0 

> Accept: */* 

>  

{ [5 bytes data] 

* TLSv1.3 (IN), TLS handshake, Newsession Ticket (4): 

{ [230 bytes data] 

* TLSv1.3 (IN), TLS handshake, Newsession Ticket (4): 

{ [230 bytes data] 

* old SSL session ID is stale, removing 

{ [5 bytes data] 

* Connection state changed (MAX_CONCURRENT_STREAMS == 256)! 

} [5 bytes data] 

< HTTP/2 302  

< date: Wed, 20 Oct 2021 16:32:58 GMT 

< content-type: text/plain 

< content-length: 733 

< cache-control: no-cache 

< location: https://storage.googleapis.com/gitlab-gprd-artifacts/c2/ 

< vary: Origin 

< x-content-type-options: nosniff 

< x-frame-options: SAMEORIGIN 

< x-request-id: 01FJF8RY782T7JQSEZHPD5W50V 

< x-runtime: 0.071994 

< strict-transport-security: max-age=31536000 

< referrer-policy: strict-origin-when-cross-origin 

< ratelimit-observed: 1 

< ratelimit-remaining: 1999 

< ratelimit-reset: 1634747638 

< ratelimit-resettime: Wed, 20 Oct 2021 16:33:58 GMT 

< ratelimit-limit: 2000 

< gitlab-lb: fe-02-lb-gprd 

< gitlab-sv: localhost 

< cf-cache-status: DYNAMIC 

< expect-ct: max-age=604800, report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct" 

< server: cloudflare 

< cf-ray: 6a13a52deb616402-ATL 

<  

* Ignoring the response-body 

{ [358 bytes data] 

100   733  100   733    0     0   2787      0 --:--:-- --:--:-- --:--:--  2787 

* Connection #0 to host gitlab.com left intact 

* Issue another request to this URL: 'https://storage.googleapis.com/gitlab-gprd-artifacts/c2/33 

* Expire in 1 ms for 1 (transfer 0x55caf3213fb0) 

* Expire in 0 ms for 1 (transfer 0x55caf3213fb0) 

  

*   Trying 172.217.204.128... 

* TCP_NODELAY set 

* Expire in 149995 ms for 3 (transfer 0x55caf3213fb0) 

* Expire in 200 ms for 4 (transfer 0x55caf3213fb0) 

* Connected to storage.googleapis.com (172.217.204.128) port 443 (#1) 

* ALPN, offering h2 

* ALPN, offering http/1.1 

* successfully set certificate verify locations: 

*   CAfile: none 

  CApath: /etc/ssl/certs 

} [5 bytes data] 

* TLSv1.3 (OUT), TLS handshake, Client hello (1): 

} [512 bytes data] 

* SSL connection using TLSv1.3 / TLS_AES_256_GCM_SHA384 

* ALPN, server accepted to use h2 

* Server certificate: 

*  subject: CN=*.storage.googleapis.com 

*  start date: Sep 13 03:01:26 2021 GMT 

*  expire date: Nov 20 03:01:25 2021 GMT 

*  subjectAltName: host "storage.googleapis.com" matched cert's "*.googleapis.com" 

*  issuer: C=US; O=Google Trust Services LLC; CN=GTS CA 1C3 

*  SSL certificate verify ok. 

* Using HTTP2, server supports multi-use 

* Connection state changed (HTTP/2 confirmed) 

* Copying HTTP/2 data in stream buffer to connection buffer after upgrade: len=0 

} [5 bytes data] 

* Using Stream ID: 1 (easy handle 0x55caf3213fb0) 

} [5 bytes data] 

> GET /gitlab-gprd-artifacts/c2/33/c23371537 

> Host: storage.googleapis.com 

> User-Agent: curl/7.64.0 

> Accept: */* 

>  

{ [5 bytes data] 

* Connection state changed (MAX_CONCURRENT_STREAMS == 100)! 

} [5 bytes data] 

< HTTP/2 200  

< x-guploader-uploadid: ADPycds4DLSFpXb3eN_zVfE4ZSlZWA3jvNSAxcBWCkhDgP6Sv5_ewLHKvDRFsHQ-A0uvR9W6l32rRWilk5urA7NoYlE 

< expires: Wed, 20 Oct 2021 16:32:58 GMT 

< date: Wed, 20 Oct 2021 16:32:58 GMT 

< cache-control: private, max-age=0 

< last-modified: Wed, 20 Oct 2021 16:31:21 GMT 

< etag: "b6e8d8734a7b3883e69baeb9c0f063bf" 

< x-goog-generation: 1634747480977957 

< x-goog-metageneration: 1 

< x-goog-stored-content-encoding: identity 

< x-goog-stored-content-length: 1337 

< content-type: application/octet-stream 

< x-goog-hash: crc32c=6OcKng== 

< x-goog-hash: md5=tujYc0p7OIPmm665wPBjvw== 

< x-goog-storage-class: MULTI_REGIONAL 

< accept-ranges: bytes 

< content-length: 1337 

< server: UploadServer 

<  

{ [5 bytes data] 

100  1337  100  1337    0     0   3991      0 --:--:-- --:--:-- --:--:--  3991 

* Connection #1 to host storage.googleapis.com left intact 

$ unzip artifacts.zip 

Archive:  artifacts.zip 

   creating: processed_values/sec-okta-prd/ 

  inflating: processed_values/sec-okta-prd/processed_values.yml   

$ mkdir /tmp/opa 

$ touch /tmp/opa.log 

$ touch /tmp/report.txt 

$ error=false 

$ cd $CI_PROJECT_DIR/opa 

$ python3 $CI_PROJECT_DIR/scripts/opa.py --log_file=/tmp/opa.log --input=$CI_PROJECT_DIR/processed_values --opa_binary=/usr/bin/opa --suite_definition=$CI_PROJECT_DIR/opa/policy_suite.yml --report_file=/tmp/report.txt || error=true 

$ if [ $error == true ]; then # collapsed multi-line command 

********* One Project Change: sec-okta-prd --> Allowed ********* 

>>> OVERALL POLICY DETAILS <<< 

data.gitops.kcc.gcp_project.cloud_connectivity          --> Allowed: True 

data.gitops.kcc.gcp_project.firewall_egress.apis        --> Allowed: True 

data.gitops.kcc.gcp_project.firewall_ingress            --> Allowed: True 

data.gitops.kcc.gcp_project.limit_bandwidth.apis        --> Allowed: True 

data.gitops.kcc.gcp_project.service.apis                --> Allowed: True 

data.gitops.kcc.gcp_project.iam.roles                   --> Allowed: True 

data.gitops.kcc.gcp_project.custom.iam.roles            --> Allowed: True 

data.gitops.kcc.gcp_project.project                     --> Allowed: True 

data.gitops.kcc.gcp_project.big.query.datasets          --> Allowed: True 

----OPA Validation Check has Passed---- 

Uploading artifacts for successful job 

00:02 

Uploading artifacts... 

opa.log: found 1 matching files and directories     

report.txt: found 1 matching files and directories  

Uploading artifacts as "archive" to coordinator... ok  id=1698855504 responseStatus=201 Created token=e-gzaJQx 

Cleaning up project directory and file based variables 

00:01 

Job succeeded 