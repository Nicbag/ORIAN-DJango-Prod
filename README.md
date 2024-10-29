# Estilo de Programación

## Convención de Nombres

### Nombres de Archivos y Carpetas

- **Archivos**: Utilizar **snake_case** para los nombres de archivos. Por ejemplo:
  - `detector.py`
  - `preprocessing.py`
  - `model_v1.pt`

- **Carpetas**: Utilizar **snake_case** para los nombres de carpetas. Por ejemplo:
  - `train_and_test/`
  - `proof_of_concept/`
  - `wagon_detection/`

### Nombres de Variables, Clases y Funciones

- **Variables**: Utilizar **snake_case** para los nombres de variables. Por ejemplo:
  - `input_image`
  - `bounding_box`
  - `confidence_score`

- **Clases**: Utilizar **CapWords** (también conocido como **CamelCase**) para los nombres de clases. Por ejemplo:
  - `ObjectDetector`
  - `ImagePreprocessor`
  - `BoundingBoxPostProcessor`

- **Métodos y funciones**: Utilizar **snake_case** para los nombres de métodos y funciones. Por ejemplo:
  - `load_model()`
  - `preprocess_image()`
  - `postprocess_results()`

## Documentación y Comentarios

### Docstrings

Utilizar docstrings para documentar módulos, clases y métodos. Los docstrings deben estar en triple comillas dobles (`"""`). Por ejemplo:
  ```python
  def load_model(model_path: str) -> Any:
      """
      Load the model from the specified path.
      
      Args:
          model_path (str): Path to the model file.
      
      Returns:
          model: Loaded model.
      """
      # Implementation here
```


### Type Hints

Utilizar type hints para mejorar la claridad del código y facilitar la detección de errores. Por ejemplo:

```python
from typing import Any

def load_model(model_path: str) -> Any:
    """
    Load the model from the specified path.
    
    Args:
        model_path (str): Path to the model file.
    
    Returns:
        model: Loaded model.
    """
    # Implementation here
```

Se debe utilizar type hints para:
* **Variables:** Incluir type hints para las variables cuando sea apropiado.
* **Funciones y Métodos:** Especificar los tipos de entrada y salida en las firmas de las funciones y métodos.

Para más información dirigirse a [Typing Library](https://docs.python.org/3/library/typing.html).

## Otras consideraciones

### Importaciones

Colocar las importaciones al inicio del archivo, ordenadas en tres grupos separadas por líneas en blanco: 
1. Importaciones estándar
2. Importaciones de terceros
3. Importaciones locales

Por ejemplo:

```python
import os
import shutil
import typing 

import matplotlib.pyplot as plt
import numpy as np
from ultralytics import YOLO

from detector1.preprocessing import preprocess
```