# 🚀 GUÍA COMPLETA: DESPLIEGUE EN RENDER

## ✅ ARCHIVOS PREPARADOS PARA RENDER:
- `requirements.txt` - Dependencias de Python
- `start.sh` - Script de inicio
- `runtime.txt` - Versión de Python
- `render.yaml` - Configuración de Render

---

## 📋 PASO A PASO PARA RENDER:

### 🔗 PASO 1: Verificar que GitHub está listo
✅ Repositorio creado: https://github.com/renealejo96/registro-cosecha-app
✅ Código subido correctamente

### 🌐 PASO 2: Crear cuenta en Render
1. Ve a: **https://render.com**
2. Click en **"Get Started for Free"**
3. **Conecta con GitHub** (recomendado)
4. Autoriza a Render para acceder a tus repositorios

### 🚀 PASO 3: Crear nuevo Web Service
1. En el dashboard, click **"New +"**
2. Selecciona **"Web Service"**
3. Conecta tu repositorio:
   - **Connect repository:** `renealejo96/registro-cosecha-app`
   - Click **"Connect"**

### ⚙️ PASO 4: Configurar el servicio
```
Name: registro-cosecha-app
Region: Oregon (US West)
Branch: main
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: ./start.sh
```

### 🔧 PASO 5: Configuraciones avanzadas
En **"Advanced"**:
```
Instance Type: Free
Auto-Deploy: Yes (recomendado)
```

### 🌟 PASO 6: Variables de entorno (Opcional)
Si necesitas configuraciones especiales:
```
STREAMLIT_SERVER_PORT = 10000
STREAMLIT_SERVER_ADDRESS = 0.0.0.0
```

### 🎯 PASO 7: Deploy!
1. Click **"Create Web Service"**
2. Render empezará el despliegue automáticamente
3. ⏱️ Espera 5-10 minutos (primera vez)

---

## 📱 RESULTADO FINAL:

### Tu aplicación estará disponible en:
```
https://registro-cosecha-app.onrender.com
```

### 🎉 PARA TUS TRABAJADORES:
1. **Comparte la URL** directamente
2. **En móvil:** Abrir navegador → Ir a la URL
3. **Crear acceso directo:** 
   - Android: "Agregar a pantalla de inicio"
   - iOS: "Agregar a pantalla de inicio"

---

## 🔍 VERIFICACIÓN:

### ✅ Checklist post-despliegue:
- [ ] La aplicación carga correctamente
- [ ] El formulario funciona en móvil
- [ ] Se pueden registrar datos
- [ ] Los gráficos se muestran bien
- [ ] La tabla es responsive

### 🛠️ Si algo falla:
1. **Ver logs en Render:** Dashboard → Logs
2. **Verificar archivos:** Todos los archivos necesarios están presentes
3. **Probar localmente:** `streamlit run app.py`

---

## 💡 CARACTERÍSTICAS DEL PLAN GRATUITO:

### ✅ Incluye:
- ✅ **750 horas/mes** (suficiente para uso normal)
- ✅ **SSL gratis** (https://)
- ✅ **Dominio personalizado**
- ✅ **Auto-deploy desde GitHub**
- ✅ **Sin límite de visitantes**

### ⚠️ Limitaciones:
- 💤 **Se "duerme" después de 15 min sin uso**
- 🔄 **Tarda ~30 segundos en "despertar"**
- 📊 **500 MB RAM máximo**

---

## 🎯 PRÓXIMOS PASOS:

1. ✅ **Desplegar en Render**
2. 📱 **Probar en móviles**
3. 👥 **Compartir URL con trabajadores**
4. 📈 **Monitorear uso y performance**

### 🔄 Para actualizaciones futuras:
- Solo hacer `git push` → Render actualiza automáticamente
- Sin necesidad de reconfigurar nada

¡Tu aplicación estará lista para producción! 🚀
