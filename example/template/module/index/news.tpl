<!--
@require common/global.css
-->
<div class="w-fil mt news">
   {% include "common/title.tpl" %}
<ul class="w-fil">
    {% for n in news %}
    <li class="w-fil news-item"><a href="{{n.url}}" class="w-fil h-fil t-ell c-fot" target="_blank">{{n.title}}</a></li>
    {% endfor %}
</ul>
</div>