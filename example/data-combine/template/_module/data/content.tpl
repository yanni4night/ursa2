
{%include "_module/data/header.tpl"%}
<ul>
    {%for g in content%}
        <li>{{loop.index}}-{{g}}</li>
    {%endfor%}
</ul>