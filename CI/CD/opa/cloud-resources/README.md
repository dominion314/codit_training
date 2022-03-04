# cloud-resources

## Tips and Tricks

Trying to figure out how your KCC resources are doing can be a pain. Take some of that pain away with this fancy custom output for your `kubectl get` command!

`kubectl get gcp --all-namespaces -o=custom-columns=NAMESPACE:.metadata.namespace,NAME:.metadata.name,KIND:.kind,STATUS:.status.conditions[0].status,REASON:.status.conditions[0].reason`

*NOTE: Getting `gcp` will pull all Config Connector resources.*

*NOTE: The `-o=custom-columns=...` provides all the extra detail. Feel free to parse out any other pieces of the resources you find to be helpful!*
