({ref})=
# {title}

``````{{ivector}} {title}
:id: "{model_name}"
:layout: {layout_type}
:template: {model_type}_template
:tags: {tags}
:language: "{language_name}"
:architecture: {architecture}
:license: "{license}"

   ```{{include}} ../../../../{model_type}/{language}/v{version}/README.md
    :start-after: "## Model details"
    :end-before: "## Installation"
   ```

   ```{{admonition}} Training corpora
   {corpora_details}
   ```

   {see_also}
``````

```{{include}} ../../../../{model_type}/{language}/v{version}/README.md
:start-after: "new)."
:end-before: "## Training data"
```
