# Variable Hierarchy
This configuration is intended to leverage the hierarchy function provided by Eunomia. You have to ensure the hierarchy.lst is properly configured as described on [here](https://github.com/KohlsTechnology/eunomia#variable-hierarchy).

## Current Hierarchy
```
team_vars
└── project_vars
```

This hierarchy presents the current default configuration commonly used by new projects. The first configuration is used as a baseline by the team at large and the second is specific to the project.

## Recommended hierarchy.lst
Adjust your relative path according to the location of your files.

The below structure assumes that you have the application definition (and hierarchy.lst) in a directory project_vars/{appName}

```
../../team_vars/{TeamName}
./
```

Including the team_vars prevents the need to repeatedly include the same set of configurations used by the team while also holding the project to common standards.

## Example hierarchy.lst
Located at gcp-config/team_vars/xpaas/ the xpaas team has defined the file iam-policy-members.yml so that the team only has to define the configurations for iam-policy once for use by their team.

The team uses variable hierarchy for the project kohls-platform-openshift-ops located at gcp-config/project_vars/ to add the predefined iam-policy to the project by including it within the hierarchy.lst as shown below.

hierarchy.lst:
```
../../default_vars
../../team_vars/xpaas
./
```

The project labels defined at /team_vars/xpaas will be added to the project as if it were defined in the project itself while still allowing the current project to add on or overwrite parts of it. Thus, this provides a more efficient organizational structure.