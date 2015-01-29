# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import sitetools.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(help_text='Creation date and time', verbose_name='Timestamp', auto_now_add=True)),
                ('name', models.CharField(help_text='Full name', max_length=150, verbose_name='Name')),
                ('email', models.EmailField(help_text='E-Mail (We will answer you to this email address)', max_length=255, verbose_name='E-Mail')),
                ('text', models.TextField(help_text='What can we help you?', verbose_name='Text')),
                ('ip', models.GenericIPAddressField(help_text='IP address', null=True, verbose_name='IP address', blank=True)),
                ('replied', models.BooleanField(default=False, help_text='Indicated if this message has been handled', verbose_name='Replied')),
                ('notes', models.TextField(help_text='Notes about this message', null=True, verbose_name='Notes', blank=True)),
            ],
            options={
                'ordering': ('-timestamp',),
                'verbose_name': 'Contact message',
                'verbose_name_plural': 'Contact messages',
            },
        ),
        migrations.CreateModel(
            name='DBTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(help_text='Template slug', unique=True, verbose_name='Slug')),
                ('content', models.TextField(help_text='Template contents', null=True, verbose_name='Content', blank=True)),
            ],
            options={
                'verbose_name': 'Database template',
                'verbose_name_plural': 'Database templates',
            },
        ),
        migrations.CreateModel(
            name='LegalDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.SlugField(help_text='Legal document unique identifier', unique=True, max_length=20, verbose_name='Identifier')),
                ('name', models.CharField(help_text='Legal document name', max_length=100, verbose_name='Name')),
                ('country', sitetools.models.fields.CountryField(choices=[(b'af', 'Afghanistan'), (b'ax', 'Aland Islands'), (b'al', 'Albania'), (b'dz', 'Algeria'), (b'as', 'American Samoa'), (b'ad', 'Andorra'), (b'ao', 'Angola'), (b'ai', 'Anguilla'), (b'aq', 'Antarctica'), (b'ag', 'Antigua and Barbuda'), (b'ar', 'Argentina'), (b'am', 'Armenia'), (b'aw', 'Aruba'), (b'au', 'Australia'), (b'at', 'Austria'), (b'az', 'Azerbaijan'), (b'bs', 'Bahamas'), (b'bh', 'Bahrain'), (b'bd', 'Bangladesh'), (b'bb', 'Barbados'), (b'by', 'Belarus'), (b'be', 'Belgium'), (b'bz', 'Belize'), (b'bj', 'Benin'), (b'bm', 'Bermuda'), (b'bt', 'Bhutan'), (b'bo', 'Bolivia'), (b'ba', 'Bosnia and Herzegovina'), (b'bw', 'Botswana'), (b'bv', 'Bouvet Island'), (b'br', 'Brazil'), (b'io', 'British indian ocean territory'), (b'bn', 'Brunei Darussalam'), (b'bg', 'Bulgaria'), (b'bf', 'Burkina Faso'), (b'bi', 'Burundi'), (b'kh', 'Cambodia'), (b'cm', 'Cameroon'), (b'ca', 'Canada'), (b'cv', 'Cape Verde'), (b'ky', 'Cayman Islands'), (b'cf', 'Central African Republic'), (b'td', 'Chad'), (b'cl', 'Chile'), (b'cn', 'China'), (b'cx', 'Christmas Island'), (b'cc', 'Cocos (Keeling) Islands'), (b'co', 'Colombia'), (b'km', 'Comoros'), (b'cg', 'Congo'), (b'cd', 'Congo, the Democratic Republic of the'), (b'ck', 'Cook islands'), (b'cr', 'Costa rica'), (b'ci', "Cote d'ivoire"), (b'hr', 'Croatia'), (b'cu', 'Cuba'), (b'cy', 'Cyprus'), (b'cz', 'Czech republic'), (b'dk', 'Denmark'), (b'dj', 'Djibouti'), (b'dm', 'Dominica'), (b'do', 'Dominican Republic'), (b'ec', 'Ecuador'), (b'eg', 'Egypt'), (b'sv', 'El salvador'), (b'gq', 'Equatorial Guinea'), (b'er', 'Eritrea'), (b'ee', 'Estonia'), (b'et', 'Ethiopia'), (b'fk', 'Falkland Islands (Malvinas)'), (b'fo', 'Faroe islands'), (b'fj', 'Fiji'), (b'fi', 'Finland'), (b'fr', 'France'), (b'gf', 'French Guiana'), (b'pf', 'French Polynesia'), (b'tf', 'French southern territories'), (b'ga', 'Gabon'), (b'gm', 'Gambia'), (b'ge', 'Georgia'), (b'de', 'Germany'), (b'gh', 'Ghana'), (b'gi', 'Gibraltar'), (b'gr', 'Greece'), (b'gl', 'Greenland'), (b'gd', 'Grenada'), (b'gp', 'Guadeloupe'), (b'gu', 'Guam'), (b'gt', 'Guatemala'), (b'gn', 'Guinea'), (b'gw', 'Guinea-bissau'), (b'gy', 'Guyana'), (b'ht', 'Haiti'), (b'hm', 'Heard Island and McDonald Islands'), (b'va', 'Holy see (Vatican City State)'), (b'hn', 'Honduras'), (b'hk', 'Hong kong'), (b'hu', 'Hungary'), (b'is', 'Iceland'), (b'in', 'India'), (b'id', 'Indonesia'), (b'ir', 'Iran, Islamic Republic of'), (b'iq', 'Iraq'), (b'ie', 'Ireland'), (b'il', 'Israel'), (b'it', 'Italy'), (b'jm', 'Jamaica'), (b'jp', 'Japan'), (b'jo', 'Jordan'), (b'kz', 'Kazakhstan'), (b'ke', 'Kenya'), (b'ki', 'Kiribati'), (b'kp', "Korea, Democratic People's Republic of"), (b'kr', 'Korea, Republic of'), (b'kw', 'Kuwait'), (b'kg', 'Kyrgyzstan'), (b'la', "Lao people's Democratic Republic"), (b'lv', 'Latvia'), (b'lb', 'Lebanon'), (b'ls', 'Lesotho'), (b'lr', 'Liberia'), (b'ly', 'Libyan Arab Jamahiriya'), (b'li', 'Liechtenstein'), (b'lt', 'Lithuania'), (b'lu', 'Luxembourg'), (b'mo', 'Macao'), (b'mk', 'Macedonia, the former Yugoslav Republic of'), (b'mg', 'Madagascar'), (b'mw', 'Malawi'), (b'my', 'Malaysia'), (b'mv', 'Maldives'), (b'ml', 'Mali'), (b'mt', 'Malta'), (b'mh', 'Marshall Islands'), (b'mq', 'Martinique'), (b'mr', 'Mauritania'), (b'mu', 'Mauritius'), (b'yt', 'Mayotte'), (b'mx', 'Mexico'), (b'fm', 'Micronesia, Federated States of'), (b'md', 'Moldova, Republic of'), (b'mc', 'Monaco'), (b'mn', 'Mongolia'), (b'ms', 'Montserrat'), (b'ma', 'Morocco'), (b'mz', 'Mozambique'), (b'mm', 'Myanmar'), (b'na', 'Namibia'), (b'nr', 'Nauru'), (b'np', 'Nepal'), (b'nl', 'Netherlands'), (b'an', 'Netherlands Antilles'), (b'nc', 'New Caledonia'), (b'nz', 'New Zealand'), (b'ni', 'Nicaragua'), (b'ne', 'Niger'), (b'ng', 'Nigeria'), (b'nu', 'Niue'), (b'nf', 'Norfolk Island'), (b'mp', 'Northern Mariana Islands'), (b'no', 'Norway'), (b'om', 'Oman'), (b'pk', 'Pakistan'), (b'pw', 'Palau'), (b'ps', 'Palestinian yerritory, occupied'), (b'pa', 'Panama'), (b'pg', 'Papua New Guinea'), (b'py', 'Paraguay'), (b'pe', 'Peru'), (b'ph', 'Philippines'), (b'pn', 'Pitcairn'), (b'pl', 'Poland'), (b'pt', 'Portugal'), (b'pr', 'Puerto Rico'), (b'qa', 'Qatar'), (b're', 'Reunion'), (b'ro', 'Romania'), (b'ru', 'Russian Federation'), (b'rw', 'Rwanda'), (b'sh', 'Saint Helena'), (b'kn', 'Saint Kitts and Nevis'), (b'lc', 'Saint Lucia'), (b'pm', 'Saint Pierre and Miquelon'), (b'vc', 'Saint Vincent and the Grenadines'), (b'ws', 'Samoa'), (b'sm', 'San marino'), (b'st', 'Sao Tome and Principe'), (b'sa', 'Saudi Arabia'), (b'sn', 'Senegal'), (b'cs', 'Serbia and Montenegro'), (b'sc', 'Seychelles'), (b'sl', 'Sierra Leone'), (b'sg', 'Singapore'), (b'sk', 'Slovakia'), (b'si', 'Slovenia'), (b'sb', 'Solomon Islands'), (b'so', 'Somalia'), (b'za', 'South Africa'), (b'gs', 'South Georgia and the south Sandwich Islands'), (b'es', 'Spain'), (b'lk', 'Sri Lanka'), (b'sd', 'Sudan'), (b'sr', 'Suriname'), (b'sj', 'Svalbard and Jan Mayen'), (b'sz', 'Swaziland'), (b'se', 'Sweden'), (b'ch', 'Switzerland'), (b'sy', 'Syrian Arab Republic'), (b'tw', 'Taiwan, province of China'), (b'tj', 'Tajikistan'), (b'tz', 'Tanzania, United Republic of'), (b'th', 'Thailand'), (b'tl', 'Timor-Leste'), (b'tg', 'Togo'), (b'tk', 'Tokelau'), (b'to', 'Tonga'), (b'tt', 'Trinidad and Tobago'), (b'tn', 'Tunisia'), (b'tr', 'Turkey'), (b'tm', 'Turkmenistan'), (b'tc', 'Turks and Caicos Islands'), (b'tv', 'Tuvalu'), (b'ug', 'Uganda'), (b'ua', 'Ukraine'), (b'ae', 'United Arab Emirates'), (b'gb', 'United Kingdom'), (b'us', 'United States'), (b'um', 'United States minor outlying islands'), (b'uy', 'Uruguay'), (b'uz', 'Uzbekistan'), (b'vu', 'Vanuatu'), (b've', 'Venezuela'), (b'vn', 'Viet nam'), (b'vg', 'Virgin Islands, british'), (b'vi', 'Virgin Islands, u.s.'), (b'wf', 'Wallis and Futuna'), (b'eh', 'Western Sahara'), (b'ye', 'Yemen'), (b'zm', 'Zambia'), (b'zw', 'Zimbabwe')], max_length=2, blank=True, help_text='Country this legal document is intended for', null=True, verbose_name='Country')),
                ('default', models.BooleanField(default=False, help_text='Default legal document', verbose_name='Default')),
                ('desc', models.TextField(help_text='Legal document description', null=True, verbose_name='Description', blank=True)),
            ],
            options={
                'verbose_name': 'Legal document',
                'verbose_name_plural': 'Legal documents',
            },
        ),
        migrations.CreateModel(
            name='LegalDocumentAcceptance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(help_text='Date and time of document acceptance', verbose_name='Timestamp', auto_now_add=True)),
                ('desc', models.CharField(help_text='Acceptance description', max_length=50, null=True, verbose_name='Description', blank=True)),
                ('ip', models.GenericIPAddressField(help_text='IP address from where the acceptance connection was made', null=True, verbose_name='IP address', blank=True)),
                ('data', models.TextField(help_text='Extra data for acceptance', null=True, verbose_name='Data', blank=True)),
            ],
            options={
                'verbose_name': 'Legal document acceptance',
                'verbose_name_plural': 'Legal document acceptances',
            },
        ),
        migrations.CreateModel(
            name='LegalDocumentVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lang', sitetools.models.fields.LanguageField(help_text='Legal document language for this version', max_length=2, verbose_name='Language', choices=[(b'es', b'Spanish')])),
                ('date', models.DateTimeField(help_text='Date and time this document will apply', verbose_name='Date')),
                ('version', models.CharField(help_text='Version number or identifier for this document', max_length=20, verbose_name='Version')),
                ('content', models.TextField(help_text='Document content', verbose_name='Content')),
                ('document', models.ForeignKey(verbose_name='Legal document', to='sitetools.LegalDocument', help_text='Legal document for this version')),
            ],
            options={
                'verbose_name': 'Legal document version',
                'verbose_name_plural': 'Legal document versions',
            },
        ),
        migrations.CreateModel(
            name='SiteInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('maintenance', models.BooleanField(default=False, help_text='Specify if this site is currently under maintenance', verbose_name='Maintenance')),
                ('active', models.BooleanField(default=False, help_text='Specifies if this site is currently active', verbose_name='Active')),
                ('site', models.OneToOneField(verbose_name='Site', to='sites.Site', help_text='Site this information is bound to')),
            ],
            options={
                'verbose_name': 'Site information',
                'verbose_name_plural': 'Site information',
            },
        ),
        migrations.CreateModel(
            name='SiteLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(help_text='Creation date', verbose_name='Created', auto_now_add=True)),
                ('level', models.PositiveIntegerField(default=1, help_text='Log level', verbose_name='Level', choices=[(1, 'Info'), (2, 'Warning'), (3, 'Error'), (4, 'Critical'), (5, 'Debug')])),
                ('tag', models.CharField(default=b'django', help_text='Tag for identifying this log message sender', max_length=20, verbose_name='Tag')),
                ('ip', models.GenericIPAddressField(default=b'0.0.0.0', help_text='Associated IP address', verbose_name='IP address')),
                ('message', models.CharField(help_text='Log message', max_length=200, verbose_name='Message')),
                ('data', sitetools.models.fields.JSONField(default=b'"null"', help_text='Extra data for log message', null=True, verbose_name='Data', blank=True)),
                ('object_id', models.PositiveIntegerField(help_text='Associated object identifier', null=True, verbose_name='Object ID', blank=True)),
                ('content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', help_text='Associated content type', null=True, verbose_name='Content type')),
                ('site', models.ForeignKey(blank=True, to='sites.Site', help_text='Associated website', null=True, verbose_name='Site')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, help_text='Associated user', null=True, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Site log',
                'verbose_name_plural': 'Site logs',
            },
        ),
        migrations.CreateModel(
            name='SiteVar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Variable name', max_length=50, verbose_name='Name')),
                ('type', models.CharField(default=b'unicode', help_text='Variable type', max_length=15, verbose_name='Type', choices=[(b'unicode', 'Unicode string'), (b'int', 'Integer'), (b'float', 'Floating point number'), (b'bool', 'Boolean'), (b'list', 'List'), (b'dict', 'Dictionary'), (b'json', 'JSON data')])),
                ('value', models.TextField(help_text='Current variable value', verbose_name='Value')),
                ('site', models.ForeignKey(verbose_name='Site', to='sitetools.SiteInfo', help_text='Site this variable is bound to')),
            ],
            options={
                'verbose_name': 'Site variable',
                'verbose_name_plural': 'Site variables',
            },
        ),
        migrations.AddField(
            model_name='legaldocumentacceptance',
            name='documentversion',
            field=models.ForeignKey(verbose_name='Version', to='sitetools.LegalDocumentVersion', help_text='Legal document version that has been accepted'),
        ),
        migrations.AddField(
            model_name='legaldocumentacceptance',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, help_text='User that accepted terms', null=True, verbose_name='User'),
        ),
        migrations.AlterUniqueTogether(
            name='legaldocumentversion',
            unique_together=set([('document', 'version')]),
        ),
    ]
