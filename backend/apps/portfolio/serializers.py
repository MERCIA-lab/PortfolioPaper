from rest_framework import serializers

from .models import Education, Experience, Portfolio, Project, Skill


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'school', 'degree', 'start_year', 'end_year']


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['id', 'company', 'role', 'start_date', 'end_date', 'description']


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'level']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'link']


class PortfolioSerializer(serializers.ModelSerializer):
    education = EducationSerializer(many=True, read_only=True)
    experience = ExperienceSerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Portfolio
        fields = ['id', 'full_name', 'job_title', 'summary', 'phone', 'email', 'location', 'photo', 'slug', 'is_public', 'created_at', 'education', 'experience', 'skills', 'projects']
        read_only_fields = ['id', 'slug', 'created_at']


class PortfolioPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ['full_name', 'job_title', 'summary', 'location', 'photo', 'slug']


class PortfolioWriteSerializer(serializers.ModelSerializer):
    education = EducationSerializer(many=True, required=False)
    experience = ExperienceSerializer(many=True, required=False)
    skills = SkillSerializer(many=True, required=False)
    projects = ProjectSerializer(many=True, required=False)

    class Meta:
        model = Portfolio
        fields = ['full_name', 'job_title', 'summary', 'phone', 'email', 'location', 'photo', 'is_public', 'education', 'experience', 'skills', 'projects']

    def update(self, instance, validated_data):
        nested_fields = ['education', 'experience', 'skills', 'projects']
        nested_payload = {field: validated_data.pop(field, None) for field in nested_fields}

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        for field_name, items in nested_payload.items():
            if items is None:
                continue

            related_model = {
                'education': Education,
                'experience': Experience,
                'skills': Skill,
                'projects': Project,
            }[field_name]

            getattr(instance, field_name).all().delete()
            for item in items:
                related_model.objects.create(portfolio=instance, **item)

        return instance
