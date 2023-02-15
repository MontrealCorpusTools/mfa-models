({ref})=
# {title}

``````{{acoustic}} {title}
:id: "{model_name}"
:layout: {layout_type}
:template: {model_type}_template
:tags: {tags}
:language: "{language_name}"
:dialect: {dialects}
:phoneset: "{phone_set}"
:architecture: {architecture}
:license: "{license}"

   ```{{include}} ../../../../{model_type}/{language}/{language_sub_folder}/v{version}/README.md
    :start-after: "## Model details"
    :end-before: "## Installation"
   ```

   ```{{admonition}} Training corpora
   {corpora_details}
   ```

   {see_also}
``````

```{{include}} ../../../../{model_type}/{language}/{language_sub_folder}/v{version}/README.md
:start-after: "new)."
:end-before: "## Training data"
```
