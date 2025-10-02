import os
import time
import logging
import threading
from datetime import datetime
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
from concurrent.futures import ThreadPoolExecutor


class ImageProcessor:
    """Classe para processamento de imagens com filtros"""
    
    def __init__(self):
        self.setup_logging()
        self.setup_directories()
    
    def setup_logging(self):
        """Configura o sistema de logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('image_processing.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_directories(self):
        """Cria diretórios necessários"""
        os.makedirs('minhas_imagens', exist_ok=True)
        os.makedirs('output', exist_ok=True)
    
    def apply_sepia_filter(self, image: Image.Image) -> Image.Image:
        """Aplica filtro sépia na imagem"""
        img_array = np.array(image)
        
        # Matriz de transformação sépia
        sepia_matrix = np.array([
            [0.393, 0.769, 0.189],
            [0.349, 0.686, 0.168],
            [0.272, 0.534, 0.131]
        ])
        
        sepia_img = np.dot(img_array, sepia_matrix.T)
        sepia_img = np.clip(sepia_img, 0, 255).astype(np.uint8)
        
        return Image.fromarray(sepia_img)
    
    def apply_vintage_filter(self, image: Image.Image) -> Image.Image:
        """Aplica filtro vintage na imagem"""
        # Aumentar contraste
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.3)
        
        # Aumentar saturação
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.2)
        
        # Aplicar blur sutil
        image = image.filter(ImageFilter.GaussianBlur(radius=0.5))
        
        # Ajustar brilho
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(0.9)
        
        return image
    
    def apply_black_white_filter(self, image: Image.Image) -> Image.Image:
        """Aplica filtro preto e branco com contraste"""
        bw_image = image.convert('L')
        enhancer = ImageEnhance.Contrast(bw_image)
        bw_image = enhancer.enhance(1.5)
        return bw_image.convert('RGB')
    
    def apply_sharpen_filter(self, image: Image.Image) -> Image.Image:
        """Aplica filtro de nitidez"""
        return image.filter(ImageFilter.SHARPEN)
    
    def apply_blur_filter(self, image: Image.Image) -> Image.Image:
        """Aplica filtro de desfoque"""
        return image.filter(ImageFilter.GaussianBlur(radius=2))
    
    def load_image_async(self, image_path: str) -> Image.Image:
        """Carrega imagem de forma assíncrona"""
        start_time = time.time()
        self.logger.info(f"[Load-Thread] Carregando imagem: {image_path}")
        
        try:
            image = Image.open(image_path)
            load_time = time.time() - start_time
            self.logger.info(f"[Load-Thread] Imagem carregada em {load_time:.3f}s - Dimensões: {image.size}")
            return image
        except Exception as e:
            self.logger.error(f"[Load-Thread] Erro ao carregar {image_path}: {str(e)}")
            raise
    
    def apply_filter_async(self, image: Image.Image, filter_name: str) -> Image.Image:
        """Aplica filtro de forma assíncrona"""
        start_time = time.time()
        self.logger.info(f"[Filter-Thread] Aplicando filtro {filter_name}")
        
        try:
            if filter_name == "sepia":
                filtered_image = self.apply_sepia_filter(image)
            elif filter_name == "vintage":
                filtered_image = self.apply_vintage_filter(image)
            elif filter_name == "black_white":
                filtered_image = self.apply_black_white_filter(image)
            elif filter_name == "sharpen":
                filtered_image = self.apply_sharpen_filter(image)
            elif filter_name == "blur":
                filtered_image = self.apply_blur_filter(image)
            else:
                raise ValueError(f"Filtro '{filter_name}' não reconhecido")
            
            filter_time = time.time() - start_time
            self.logger.info(f"[Filter-Thread] Filtro {filter_name} aplicado em {filter_time:.3f}s")
            return filtered_image
            
        except Exception as e:
            self.logger.error(f"[Filter-Thread] Erro ao aplicar filtro {filter_name}: {str(e)}")
            raise
    
    def save_image_async(self, image: Image.Image, output_path: str) -> None:
        """Salva imagem de forma assíncrona"""
        start_time = time.time()
        self.logger.info(f"[Save-Thread] Salvando imagem: {output_path}")
        
        try:
            image.save(output_path, quality=95)
            save_time = time.time() - start_time
            self.logger.info(f"[Save-Thread] Imagem salva em {save_time:.3f}s")
        except Exception as e:
            self.logger.error(f"[Save-Thread] Erro ao salvar {output_path}: {str(e)}")
            raise
    
    def process_single_image_parallel(self, image_path: str, filter_name: str, output_path: str) -> dict:
        """Processa uma única imagem com paralelismo interno"""
        start_time = time.time()
        
        self.logger.info(f"Iniciando processamento de {image_path} com filtro {filter_name}")
        
        try:
            # Usar ThreadPoolExecutor para paralelismo interno
            with ThreadPoolExecutor(max_workers=3, thread_name_prefix="Worker") as executor:
                # Carregar imagem
                load_future = executor.submit(self.load_image_async, image_path)
                
                # Aguardar carregamento
                image = load_future.result()
                
                # Aplicar filtro
                filter_future = executor.submit(self.apply_filter_async, image, filter_name)
                filtered_image = filter_future.result()
                
                # Salvar imagem
                save_future = executor.submit(self.save_image_async, filtered_image, output_path)
                save_future.result()
            
            total_time = time.time() - start_time
            
            result = {
                'input_path': image_path,
                'output_path': output_path,
                'filter_name': filter_name,
                'image_size': image.size,
                'total_time': total_time,
                'success': True,
                'timestamp': datetime.now().isoformat()
            }
            
            self.logger.info(f"Processamento concluído em {total_time:.3f}s")
            return result
            
        except Exception as e:
            error_time = time.time() - start_time
            self.logger.error(f"Erro ao processar {image_path}: {str(e)}")
            
            result = {
                'input_path': image_path,
                'output_path': output_path,
                'filter_name': filter_name,
                'error': str(e),
                'total_time': error_time,
                'success': False,
                'timestamp': datetime.now().isoformat()
            }
            
            return result


def main():
    """Função principal para processamento de imagem única"""
    import sys
    
    if len(sys.argv) < 3:
        print("❌ Uso: python image_processor.py <imagem> <filtro>")
        print("💡 Exemplo: python image_processor.py foto.jpg sepia")
        print("\n🔧 Filtros disponíveis:")
        print("  sepia, vintage, black_white, sharpen, blur")
        return
    
    image_path = sys.argv[1]
    filter_name = sys.argv[2]
    
    # Verificar se arquivo existe
    if not os.path.exists(image_path):
        print(f"❌ Arquivo não encontrado: {image_path}")
        return
    
    # Verificar se filtro é válido
    valid_filters = ["sepia", "vintage", "black_white", "sharpen", "blur"]
    if filter_name not in valid_filters:
        print(f"❌ Filtro inválido: {filter_name}")
        print(f"💡 Filtros válidos: {', '.join(valid_filters)}")
        return
    
    print("🎨 PROCESSADOR DE IMAGENS")
    print("=" * 50)
    
    # Criar processador
    processor = ImageProcessor()
    
    # Definir caminho de saída
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    output_path = f"output/{base_name}_{filter_name}.jpg"
    
    print(f"📸 Processando: {os.path.basename(image_path)}")
    print(f"🎨 Filtro: {filter_name}")
    print(f"💾 Saída: {output_path}")
    print("\n⏱️  Iniciando processamento...")
    
    # Processar
    start_time = time.time()
    result = processor.process_single_image_parallel(image_path, filter_name, output_path)
    total_time = time.time() - start_time
    
    # Mostrar resultados
    if result['success']:
        print(f"\n✅ SUCESSO!")
        print(f"⏱️  Tempo total: {result['total_time']:.3f}s")
        print(f"📐 Dimensões: {result['image_size']}")
        print(f"📁 Arquivo: {result['output_path']}")
    else:
        print(f"\n❌ ERRO: {result['error']}")
        print(f"⏱️  Tempo até erro: {result['total_time']:.3f}s")
    
    print(f"\n📊 Logs: image_processing.log")
    print(f"📁 Resultado: output/")


if __name__ == "__main__":
    main()
