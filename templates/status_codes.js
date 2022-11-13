{% for items in codes %}
    const {{items.name}}_codes = {
        {% for item in items.data %}
        '{{ item.key }}':{
            key: '{{ item.key }}',
            value: '{{ item.value }}' 
        },
        {% endfor %}
    };
{% endfor %}
