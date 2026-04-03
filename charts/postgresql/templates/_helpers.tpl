{{/*
chartName:
*/}}
{{- define "postgre.name" -}}
{{- .Chart.Name -}}
{{- end }}

{{/*
fullName: [RELEASE]-[CHART]
*/}}
{{- define "postgre.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end }}


{{/*
commonLabels:
*/}}
{{- define "postgre.labels" -}}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version | replace "+" "_" }}
app.kubernetes.io/name: {{ include "postgre.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
selectorLabels:
*/}}
{{- define "postgre.selectorLabels" -}}
app.kubernetes.io/name: {{ include "postgre.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
