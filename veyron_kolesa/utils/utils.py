from rest_framework import serializers


class ChoiceValueDisplayField(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        return data

    def get_attribute(self, instance):
        try:
            attr = self.source
            display_method = getattr(instance, 'get_%s_display' % attr)

            # value = getattr(instance, attr)
            display_value = display_method()

            return display_value
            # return {
            #     'value': value,
            #     'display': display_value
            # }
        except Exception as e:
            print(e)
            return super(ChoiceValueDisplayField, self).get_attribute(instance)
