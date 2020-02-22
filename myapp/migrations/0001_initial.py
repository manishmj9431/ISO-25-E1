# Generated by Django 3.0.3 on 2020-02-22 20:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Colleges',
            fields=[
                ('college_id', models.AutoField(primary_key=True, serialize=False)),
                ('college_name', models.CharField(max_length=50)),
                ('university', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=200)),
                ('contact_number', models.CharField(max_length=15)),
                ('logo', models.ImageField(upload_to='logos/')),
                ('about_us', models.TextField(max_length=1000)),
                ('image1', models.ImageField(upload_to='slider/')),
                ('image2', models.ImageField(null=True, upload_to='slider/')),
                ('image3', models.ImageField(null=True, upload_to='slider/')),
                ('image4', models.ImageField(null=True, upload_to='slider/')),
                ('image5', models.ImageField(null=True, upload_to='slider/')),
            ],
        ),
        migrations.CreateModel(
            name='Departments',
            fields=[
                ('department_id', models.AutoField(primary_key=True, serialize=False)),
                ('department_name', models.CharField(max_length=50)),
                ('vision_mission', models.TextField(max_length=1000)),
                ('college_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Colleges')),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('roll_number', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('semester', models.IntegerField()),
                ('college_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Colleges')),
                ('department_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Departments')),
            ],
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('subject_id', models.AutoField(primary_key=True, serialize=False)),
                ('subject_name', models.CharField(max_length=50)),
                ('semester', models.IntegerField()),
                ('college_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Colleges')),
                ('department_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Departments')),
            ],
        ),
        migrations.CreateModel(
            name='Teachers',
            fields=[
                ('teacher_id', models.AutoField(primary_key=True, serialize=False)),
                ('teacher_name', models.CharField(max_length=50)),
                ('college_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Colleges')),
                ('department_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Departments')),
            ],
        ),
        migrations.CreateModel(
            name='SyllabusStatusTeacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.IntegerField()),
                ('college_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Colleges')),
                ('department_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Departments')),
                ('given_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Teachers')),
                ('subject_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Subjects')),
            ],
        ),
        migrations.CreateModel(
            name='SyllabusStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.IntegerField()),
                ('college_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Colleges')),
                ('department_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Departments')),
                ('given_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Students')),
                ('subject_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Subjects')),
            ],
        ),
        migrations.CreateModel(
            name='Syllabus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.IntegerField()),
                ('unit_name', models.CharField(max_length=10)),
                ('topics', models.TextField(max_length=1000)),
                ('college_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Colleges')),
                ('department_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Departments')),
                ('subject_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Subjects')),
            ],
        ),
        migrations.AddField(
            model_name='subjects',
            name='taught_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.Teachers'),
        ),
    ]
