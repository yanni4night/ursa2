{% extends "parent.tpl" %}

{% block page_title %}Ursa2 Example{% endblock %}
{% block content %}

<div class="content w-cen">
{% include "module/index/header.tpl" %}
{% include "module/index/search.tpl" %}
{% set title = "Top News" %}
{% include "module/index/news.tpl" %}

{% set title = "Social News" %}
{% include "module/index/news.tpl" %}
</div>
{% endblock %}
