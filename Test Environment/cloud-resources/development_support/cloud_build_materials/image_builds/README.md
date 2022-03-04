# Buildiung container images in CloudBuild
## The purpose
Cloud Build allows flexibility that allows automation pipeline to specify a dedicated underlying container image to support each step (stage) of pipeline. A collection of pre-built quality images is available to CB processes immediatelly by GCP https://console.cloud.google.com/gcr/images/cloud-builders/GLOBAL

It might be beneficial - to allow for faster built time and because of management strategy, to allow CB to build custom images and make those available to other CB processes.

## Process 
General documentation on process of building and storing custom images using CB is available here: https://cloud.google.com/cloud-build/docs/building/build-containers

### Examples:
Examples of how to build some of the images utilized in KCC effort are available in **image_builds/images/** folder

## Storage 
Custom built images are stored in Container Registry of the project that has CB enabled in.
Those images can be refered to immediatelly by another cloud build process.

## Concerns
For reasons of enforcing uniform security and corporate policies it is seem to be beneficial to allow CB process to utilize Docker container images produced and vetteed by Kohls and stored in appropriate corporate container registry. Currently two options appear to be worth validating: 
    - Ability of CB process to 'pull' container image into CB worker space must be validated. 
    - Synchronization of certain images from Kohls repository to GCP Container Registry