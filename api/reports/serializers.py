from rest_framework import serializers

from api.reports.models import ReportReasons


class ReportReasonSerializer(serializers.ModelSerializer):

    class Meta:

        model = ReportReasons

        fields = ('id', 'name')