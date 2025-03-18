import sys
from datetime import datetime
from validacion_credenciales import *

# Cuenta Caracteres
def cuentaCaracteres():
	codigo_java = """package us.dit;

public class Control {

    public static void main(String[] args) {
        System.out.println(cuentaCaracteres("Hola"));
    }
    
    public static int cuentaCaracteres(String texto) {
        return texto.length();
    }
}
"""

	# Imprimir el código Java en la salida estándar
	return(codigo_java)


# Contar vocales
def cuentaVocales():

	codigo_java="""package us.dit;

public class Control {

    public static void main(String[] args) {
        System.out.println(contarVocales("Hola"));
    }
    
    public static int contarVocales(String texto) {
       
        int contador = 0;
        texto = texto.toLowerCase(); // Convertir todo a minúsculas para simplificar
        
        for (char c : texto.toCharArray()) {
            if ("aeiou".indexOf(c) != -1) { // Verifica si el carácter es una vocal
                contador++;
            }
        }
        return contador;
    }
}
"""

	return(codigo_java)

def vocalespar():

	codigo_java = """ package us.dit;

public class Control {

    public static void main(String[] args) {
        System.out.println(esNumeroVocalesPar("Hola"));
    }
    
    public static boolean esNumeroVocalesPar(String texto) {
        
        int contador = 0;
        texto = texto.toLowerCase(); // Convertimos a minúsculas para evitar problemas
        
        for (char c : texto.toCharArray()) {
            if ("aeiou".indexOf(c) != -1) { // Verificamos si el carácter es una vocal
                contador++;
            }
        }
        
        return contador % 2 == 0; // Devuelve true si el número de vocales es par, false si es impar
    }
}"""
	return(codigo_java)

def palindroma():

	codigo_java = """package us.dit;

public class Control {

    public static void main(String[] args) {
        System.out.println(esPalindromo("Hola"));
    }
    
    public static boolean esPalindromo(String texto) {
    	// Convertir a minúsculas y eliminar espacios en blanco
        texto = texto.toLowerCase().replaceAll("\\s+", "");

        int izquierda = 0;
        int derecha = texto.length() - 1;

        while (izquierda < derecha) {
            if (texto.charAt(izquierda) != texto.charAt(derecha)) {
                return false; // Si no coinciden, no es un palíndromo
            }
            izquierda++;
            derecha--;
        }

        return true; // Si recorremos toda la palabra sin diferencias, es palíndromo
    }
}"""

	return(codigo_java)

#######

# Cuenta Caracteres
def convertirAMayusculasEInvertir():
	codigo_java = """package us.dit;

public class Control {

    public static void main(String[] args) {
        System.out.println(convertirAMayusculasEInvertir("Hola"));
    }
    
    public static String convertirAMayusculasEInvertir(String texto) {
        String mayusculas = texto.toUpperCase(); // Convierte la cadena a mayúsculas
        return new StringBuilder(mayusculas).reverse().toString(); // Invierte la cadena y la devuelve
    }
}
"""

	# Imprimir el código Java en la salida estándar
	return(codigo_java)


# Contar vocales
def contarVocales():

	codigo_java="""package us.dit;  

public class Control {

    public static void main(String[] args) {
        System.out.println(contarVocales("Qué hay de nuevo viejo"));
    }
    
    public static int contarVocales(String texto) {
        int contador = 0;
        texto = texto.toLowerCase(); // Convertimos a minúsculas para evitar problemas
        
        for (char c : texto.toCharArray()) {
            if ("aeiouáéíóú".indexOf(c) != -1) { // Verificamos si el carácter es una vocal
                contador++;
            }
        }
        
        return contador; // Devuelve el número de vocales en la cadena
    }
}
"""

	return(codigo_java)

def contarConsonantes():

	codigo_java = """package us.dit;

public class Control {

    public static void main(String[] args) {
        System.out.println(contarConsonantes("Cálmate"));
    }
    
    public static int contarConsonantes(String texto) {
        int contador = 0;
        texto = texto.toLowerCase(); // Convertimos a minúsculas para evitar problemas
        
        for (char c : texto.toCharArray()) {
            if (Character.isLetter(c) && "aeiouáéíóú".indexOf(c) == -1) { // Verificamos si es letra y no es vocal
                contador++;
            }
        }
        
        return contador; // Devuelve el número de consonantes en la cadena
    }
}
"""
	return(codigo_java)

def intercambiarMayusculasMinusculas():

	codigo_java = """package us.dit;

public class Control {

    public static void main(String[] args) {
        System.out.println(intercambiarMayusculasMinusculas("EEUU de América"));
    }
    
    public static String intercambiarMayusculasMinusculas(String texto) {
        StringBuilder resultado = new StringBuilder();
        
        for (char c : texto.toCharArray()) {
            if (Character.isUpperCase(c)) {
                resultado.append(Character.toLowerCase(c));
            } else if (Character.isLowerCase(c)) {
                resultado.append(Character.toUpperCase(c));
            } else {
                resultado.append(c);
            }
        }
        
        return resultado.toString(); // Devuelve la cadena con mayúsculas y minúsculas intercambiadas
    }
}
"""

	return(codigo_java)

def eliminarTildes():

	codigo_java = """package us.dit;

public class Control {

    public static void main(String[] args) {
        System.out.println(eliminarTildes("Canción, árbol, café"));
    }
    
    public static String eliminarTildes(String texto) {
        texto = texto.replace("á", "a").replace("é", "e").replace("í", "i")
                     .replace("ó", "o").replace("ú", "u")
                     .replace("Á", "A").replace("É", "E").replace("Í", "I")
                     .replace("Ó", "O").replace("Ú", "U");
        return texto; // Devuelve la cadena sin tildes
    }
}
"""
	return(codigo_java)

def fibonacci():

	codigo_java = """package us.dit;

public class Control {

    public static void main(String[] args) {
        int n = 10; // Número de términos que quieres generar en la sucesión

        System.out.println("Sucesión de Fibonacci hasta el término " + n + ":");

        for (int i = 0; i < n; i++) {
            System.out.print(fibonacci(i) + " ");
        }
    }

    // Método recursivo para calcular el enésimo término de la sucesión de Fibonacci
    public static int fibonacci(int num) {
        if (num <= 1) {
            return num;
        } else {
            return fibonacci(num - 1) + fibonacci(num - 2);
        }
    }
}
"""

	return(codigo_java)



def factorial():

	codigo_java = """package us.dit;

public class Control {

    public static void main(String[] args) {
        int numero = 5; 
        int resultado = factorial(numero);

        System.out.println("El factorial de " + numero + " es: " + resultado);
    }

    // Calcular el factorial de un número
    public static int factorial(int num) {
        if (num == 0) {
            return 1; // El factorial de 0 es 1
        } else {
            return num * factorial(num - 1);
        }
    }
}
"""

	return(codigo_java)



def esPrimo():

	codigo_java = """package us.dit;

public class Control {

    public static void main(String[] args) {
        int numero = 29; // Número para verificar si es primo
        boolean esPrimo = esPrimo(numero);

        if (esPrimo) {
            System.out.println(numero + " es un número primo.");
        } else {
            System.out.println(numero + " no es un número primo.");
        }
    }

    // Método para verificar si un número es primo
    public static boolean esPrimo(int num) {
        if (num <= 1) {
            return false;
        }
        for (int i = 2; i <= Math.sqrt(num); i++) {
            if (num % i == 0) {
                return false; 
            }
        }
        return true;
    }
}
"""

	return(codigo_java)


def suma_ascii(texto: str) -> int:
    return sum(ord(c) for c in texto)%10


dt = datetime.now()
ts = datetime.timestamp(dt)

# generar el hash (uvus + timestamp)
hash_generado = crear_identificador(sys.argv[1], str(ts))

# Fecha objetivo: 6 de marzo de 2025 a las 13:00 AM
fecha_objetivo = datetime(2025, 3, 6, 13, 0)

# Fecha actual
fecha_actual = datetime.now()

try:
    if len(sys.argv) != 3:
        print("El formato esperado es: ./generaPregunta suUvus grupoControl")
        # grupo del alumno
           

    else:   
        grupo = int(sys.argv[2])

        if (grupo not in [1,2,3]):
            print("Nº grupo incorrecto, grupoControl -> [1,2,3]")
           
        else:
            resultado = suma_ascii(sys.argv[1])
            
            # Para el martes
            if grupo == 1:

                if resultado <= 2:
                    resultado_str = cuentaCaracteres()
                elif 3 <= resultado <= 5:
                    resultado_str = cuentaVocales()
                elif 6 <= resultado <= 8:
                    resultado_str = vocalespar()
                else:
                    resultado_str = palindroma()

                resultado_str = "//uvus:" +sys.argv[1] + "\n//pass:"+ str(hash_generado)+"\n\n" + resultado_str 

                with open("claseControl.txt", "w", encoding="utf-8") as archivo:
                    archivo.write(resultado_str)
                    print("La clase Control se ha generado correctamente, puede encontrarla en claseControl.txt")

            # Condicion para el jueves
            elif grupo == 2:
            
                if resultado <= 2:
                    resultado_str = convertirAMayusculasEInvertir()
                elif 3 <= resultado <= 5:
                    resultado_str = contarVocales()
                elif 6 <= resultado <= 8:
                    resultado_str = contarConsonantes()
                else:
                    resultado_str = intercambiarMayusculasMinusculas()

                resultado_str = "//uvus:" +sys.argv[1] + "\n//pass:"+ str(hash_generado)+"\n\n" + resultado_str 

                with open("claseControl.txt", "w", encoding="utf-8") as archivo:
                    archivo.write(resultado_str)
                    print("La clase Control se ha generado correctamente, puede encontrarla en claseControl.txt")
            # Condicion para el viernes	
            elif grupo == 3:

                if resultado <= 2:
                    resultado_str = eliminarTildes()
                elif 3 <= resultado <= 5:
                    resultado_str = fibonacci()
                elif 6 <= resultado <= 8:
                    resultado_str = factorial()
                else:
                    resultado_str = esPrimo()

                resultado_str = "//uvus:" +sys.argv[1] + "\n//pass:"+ str(hash_generado)+"\n\n" + resultado_str 

                with open("claseControl.txt", "w", encoding="utf-8") as archivo:
                    archivo.write(resultado_str)
                    print("La clase Control se ha generado correctamente, puede encontrarla en claseControl.txt")

except:
    print("grupoControl introducido en formato incorrecto")
  

    
        



