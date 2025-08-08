# 🛠️ SOLUCIÓN DE PROBLEMAS - RENDER

## ❌ ERROR: "El directorio raíz 'main' no existe"

### 🔍 **CAUSA DEL PROBLEMA:**
Render está confundiendo el nombre de la rama con el directorio raíz.

### ✅ **SOLUCIÓN PASO A PASO:**

#### 1. **En la configuración de Render:**
```
❌ INCORRECTO:
Root Directory: main

✅ CORRECTO:
Root Directory: .
```

#### 2. **Configuración completa correcta:**
```
Name: registro-cosecha-app
Region: Oregon (US West)
Branch: main                    ← Esto es la RAMA de Git
Runtime: Python 3
Root Directory: .               ← Esto es el DIRECTORIO (solo un punto)
Build Command: pip install -r requirements.txt
Start Command: streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true --server.fileWatcherType none
```

#### 3. **Si el error persiste:**
- Borra el servicio en Render
- Crea uno nuevo con la configuración correcta
- Asegúrate de que el repositorio esté público en GitHub

---

## 🔄 **MÉTODOS ALTERNATIVOS:**

### **OPCIÓN A: Usar Procfile**
Si `start.sh` causa problemas, Render puede usar automáticamente el `Procfile`:
```
Build Command: pip install -r requirements.txt
Start Command: (dejar vacío - usará Procfile automáticamente)
```

### **OPCIÓN B: Usar render.yaml**
Render puede usar el archivo `render.yaml` automáticamente si está en la raíz del proyecto.

---

## 🚨 **OTROS PROBLEMAS COMUNES:**

### **ERROR: "No se puede ejecutar start.sh"**
**Solución:** Usar directamente el comando de Streamlit:
```
Start Command: streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
```

## ❌ ERROR: "Cannot import 'setuptools.build_meta'"

### 🔍 **CAUSA DEL PROBLEMA:**
Versión incompatible o corrupta de setuptools durante el build.

### ✅ **SOLUCIÓN PASO A PASO:**

#### 1. **Build Command robusto:**
```
python -m pip install --upgrade pip>=22.0.0 && python -m pip install --upgrade setuptools>=65.0.0 wheel>=0.38.0 && python -m pip install --no-cache-dir --prefer-binary --timeout 1000 -r requirements.txt
```

#### 2. **Variables de entorno necesarias:**
```
PIP_NO_CACHE_DIR = 1
PIP_PREFER_BINARY = 1
SETUPTOOLS_USE_DISTUTILS = stdlib
```

#### 3. **Si el error persiste:**
- Borra el servicio en Render completamente
- Crea uno nuevo con la configuración actualizada
- Usa Python 3.11 (no 3.12 que puede tener problemas)

---

### **ERROR: "Failed building wheel for pandas"**
**Causa:** Problemas de compilación de pandas en el servidor de Render
**Solución:** 
1. Usar Build Command optimizado:
```
python -m pip install --upgrade pip setuptools wheel && pip install --no-cache-dir --prefer-binary -r requirements.txt
```
2. Agregar variables de entorno:
```
PIP_NO_CACHE_DIR = 1
PIP_PREFER_BINARY = 1
```
3. Si persiste, usar versiones específicas en requirements.txt (ya incluidas)

### **ERROR: "Módulo no encontrado"**
**Solución:** Verificar que `requirements.txt` esté correcto:
```
streamlit==1.28.0
pandas==2.0.3
altair==5.0.1
```

### **ERROR: "Puerto no disponible"**
**Solución:** Asegurarse de usar `$PORT` en el comando:
```
--server.port $PORT
```

---

## ✅ **VERIFICACIÓN FINAL:**

Después del despliegue exitoso, verifica:
1. **URL funciona:** https://tu-app.onrender.com
2. **Formulario carga** correctamente
3. **Se pueden registrar datos**
4. **Gráficos se muestran**
5. **Responsive en móvil**

---

## 📞 **SI NADA FUNCIONA:**

### **Plan B - Streamlit Community Cloud:**
1. Ve a: https://share.streamlit.io
2. Conecta GitHub
3. Selecciona tu repositorio
4. ¡Deploy automático en 2 minutos!

**Ventaja:** Especializado en Streamlit, casi nunca falla.

---

¡Con esta solución tu aplicación debería desplegarse correctamente! 🚀
