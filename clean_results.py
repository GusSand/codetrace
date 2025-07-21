#!/usr/bin/env python3
import json
import sys
from pathlib import Path
import gc
import ijson  # For memory-efficient JSON parsing
import psutil  # For memory monitoring
import time
import logging
from datetime import datetime
import os

def setup_logging(output_dir):
    """Setup logging configuration."""
    # Create logs directory if it doesn't exist
    log_dir = Path(output_dir).parent / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Create a log file with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = log_dir / f'clean_results_{timestamp}.log'
    
    # Configure logging with more detailed format
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - [%(processName)s:%(process)d] - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Log system information
    logging.info("=== System Information ===")
    logging.info(f"Python version: {sys.version}")
    logging.info(f"Operating system: {os.uname()}")
    logging.info(f"CPU count: {os.cpu_count()}")
    mem = psutil.virtual_memory()
    logging.info(f"Total system memory: {mem.total / (1024**3):.2f} GB")
    logging.info(f"Available memory: {mem.available / (1024**3):.2f} GB")
    logging.info("========================")
    
    return log_file

def get_memory_usage():
    """Get current memory usage in MB."""
    process = psutil.Process()
    return process.memory_info().rss / 1024 / 1024

def clean_result_object(obj):
    """Remove large unnecessary data from a result object."""
    keys_to_remove = [
        'logits',
        'hidden_states',
        'attentions',
        'cross_attentions',
        'past_key_values',
        'encoder_hidden_states',
        'encoder_attentions',
        'intermediate_states',
        'last_hidden_state',
        'all_hidden_states',
        'all_attentions',
        'all_cross_attentions'
    ]
    
    removed_keys = []
    original_size = sys.getsizeof(str(obj)) if obj else 0
    
    if isinstance(obj, dict):
        cleaned = {}
        for k, v in obj.items():
            if k not in keys_to_remove:
                cleaned[k] = clean_result_object(v)
            else:
                removed_keys.append(k)
        
        # Log details about removed keys if any were found
        if removed_keys:
            logging.debug(f"Removed keys from object: {', '.join(removed_keys)}")
        
        cleaned_size = sys.getsizeof(str(cleaned))
        if original_size > 1024 * 1024:  # Only log if original size > 1MB
            logging.debug(f"Object size reduction: {original_size/1024/1024:.2f}MB -> {cleaned_size/1024/1024:.2f}MB")
        
        return cleaned
    elif isinstance(obj, list):
        return [clean_result_object(item) for item in obj]
    else:
        return obj

def log_memory_stats():
    """Log detailed memory statistics."""
    process = psutil.Process()
    mem_info = process.memory_info()
    
    logging.info("=== Memory Statistics ===")
    logging.info(f"  RSS (Resident Set Size): {mem_info.rss / 1024 / 1024:.2f} MB")
    logging.info(f"  VMS (Virtual Memory Size): {mem_info.vms / 1024 / 1024:.2f} MB")
    if hasattr(mem_info, 'shared'):
        logging.info(f"  Shared Memory: {mem_info.shared / 1024 / 1024:.2f} MB")
    if hasattr(mem_info, 'data'):
        logging.info(f"  Data Segment: {mem_info.data / 1024 / 1024:.2f} MB")
    
    # Add CPU usage information
    cpu_percent = process.cpu_percent()
    logging.info(f"  CPU Usage: {cpu_percent:.1f}%")
    
    # Add garbage collector statistics
    gc_counts = gc.get_count()
    logging.info(f"  GC Counts: {gc_counts}")
    
    # Add system memory information
    sys_memory = psutil.virtual_memory()
    logging.info(f"  System Memory Usage: {sys_memory.percent:.1f}%")
    logging.info(f"  Available System Memory: {sys_memory.available / (1024**3):.2f} GB")
    logging.info("======================")

def process_file(input_file, output_file, chunk_size=1):
    """Process a large JSON file in chunks, removing unnecessary data."""
    # Setup logging
    log_file = setup_logging(output_file)
    logging.info(f"Starting processing of {input_file}")
    logging.info(f"Output will be saved to {output_file}")
    logging.info(f"Log file: {log_file}")
    
    start_time = time.time()
    input_size = Path(input_file).stat().st_size / (1024 * 1024 * 1024)  # Size in GB
    logging.info(f"Input file size: {input_size:.2f} GB")
    
    # Log initial memory state
    logging.info("Initial memory state:")
    log_memory_stats()
    
    # Create output directory if it doesn't exist
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    
    total_objects = 0
    current_chunk = []
    last_progress_time = time.time()
    objects_since_last_progress = 0
    total_keys_removed = 0
    total_size_reduction = 0
    total_events = 0
    last_event_time = time.time()
    
    try:
        # Use ijson to parse the file incrementally
        logging.info("Starting file parsing with ijson...")
        with open(input_file, 'rb') as f:
            parser = ijson.parse(f)
            current_obj = {}
            chunk_start_time = time.time()
            last_gc_time = time.time()
            parsing_depth = 0
            
            for prefix, event, value in parser:
                total_events += 1
                current_time = time.time()
                
                # Log parsing progress every 60 seconds
                if current_time - last_event_time >= 60:
                    elapsed = current_time - start_time
                    events_per_sec = total_events / elapsed
                    bytes_processed = f.tell()
                    progress_gb = bytes_processed / (1024**3)
                    progress_pct = (bytes_processed / (input_size * 1024**3)) * 100
                    
                    logging.info(
                        f"=== Parsing Progress ===\n"
                        f"Events processed: {total_events:,}\n"
                        f"Processing rate: {events_per_sec:.2f} events/second\n"
                        f"Bytes processed: {bytes_processed:,} ({progress_gb:.2f} GB)\n"
                        f"Progress: {progress_pct:.2f}%\n"
                        f"Current parsing depth: {parsing_depth}\n"
                        f"Current memory usage: {get_memory_usage():.2f} MB"
                    )
                    last_event_time = current_time
                
                if event == 'start_map':
                    parsing_depth += 1
                    if prefix == '':
                        current_obj = {}
                        logging.debug(f"Started new object (depth: {parsing_depth})")
                elif event == 'end_map':
                    parsing_depth -= 1
                    if prefix == '':
                        # Clean and store the object
                        original_size = sys.getsizeof(str(current_obj))
                        cleaned_obj = clean_result_object(current_obj)
                        cleaned_size = sys.getsizeof(str(cleaned_obj))
                        size_reduction = original_size - cleaned_size
                        total_size_reduction += size_reduction
                        
                        if original_size > 1024 * 1024:  # Log if object was > 1MB
                            logging.info(f"Large object processed: {original_size/1024/1024:.2f}MB -> {cleaned_size/1024/1024:.2f}MB")
                        
                        current_chunk.append(cleaned_obj)
                        total_objects += 1
                        objects_since_last_progress += 1
                        
                        # Print progress with memory usage every 10 objects or 60 seconds
                        current_time = time.time()
                        if total_objects % 10 == 0 or (current_time - last_progress_time) >= 60:
                            elapsed_time = current_time - start_time
                            memory_usage = get_memory_usage()
                            processing_rate = objects_since_last_progress / (current_time - last_progress_time)
                            
                            logging.info(
                                f"=== Progress Update ===\n"
                                f"Objects processed: {total_objects}\n"
                                f"Processing rate: {processing_rate:.2f} objects/second\n"
                                f"Memory usage: {memory_usage:.2f} MB\n"
                                f"Elapsed time: {elapsed_time:.2f}s\n"
                                f"Total size reduction: {total_size_reduction/1024/1024:.2f}MB\n"
                                f"Average reduction per object: {(total_size_reduction/total_objects)/1024:.2f}KB"
                            )
                            
                            last_progress_time = current_time
                            objects_since_last_progress = 0
                            log_memory_stats()
                        
                        # Periodic garbage collection (every 5 minutes)
                        if current_time - last_gc_time >= 300:
                            logging.info("Running garbage collection...")
                            gc_count_before = gc.get_count()
                            gc.collect()
                            gc_count_after = gc.get_count()
                            logging.info(f"GC counts before: {gc_count_before}, after: {gc_count_after}")
                            last_gc_time = current_time
                        
                        # Write chunk if it reaches the specified size
                        if len(current_chunk) >= chunk_size:
                            chunk_time = time.time() - chunk_start_time
                            chunk_size_mb = sum(sys.getsizeof(str(obj)) for obj in current_chunk) / 1024 / 1024
                            logging.info(f"Writing chunk: {len(current_chunk)} objects, {chunk_size_mb:.2f}MB (took {chunk_time:.2f}s)")
                            write_chunk(current_chunk, output_file, total_objects == chunk_size)
                            current_chunk = []
                            gc.collect()
                            chunk_start_time = time.time()
                
                elif event in ('string', 'number', 'boolean', 'null'):
                    # Build the current object
                    obj = current_obj
                    parts = prefix.split('.')
                    for part in parts[:-1]:
                        if part.isdigit():
                            idx = int(part)
                            if len(obj) <= idx:
                                obj.extend([{} for _ in range(idx - len(obj) + 1)])
                            obj = obj[idx]
                        else:
                            if part not in obj:
                                obj[part] = {}
                            obj = obj[part]
                    
                    last_part = parts[-1] if parts else prefix
                    if last_part:
                        if last_part.isdigit():
                            idx = int(last_part)
                            if isinstance(obj, dict):
                                obj = []
                            if len(obj) <= idx:
                                obj.extend([None for _ in range(idx - len(obj) + 1)])
                            obj[idx] = value
                        else:
                            obj[last_part] = value
        
        # Write any remaining objects
        if current_chunk:
            chunk_size_mb = sum(sys.getsizeof(str(obj)) for obj in current_chunk) / 1024 / 1024
            logging.info(f"Writing final chunk: {len(current_chunk)} objects, {chunk_size_mb:.2f}MB")
            write_chunk(current_chunk, output_file, total_objects == len(current_chunk))
        
        end_time = time.time()
        total_time = end_time - start_time
        
        try:
            output_size = Path(output_file).stat().st_size / (1024 * 1024 * 1024)  # Size in GB
            size_reduction_pct = (1 - output_size/input_size) * 100
        except FileNotFoundError:
            logging.warning("Could not read output file size - file may still be being written")
            output_size = 0
            size_reduction_pct = 0
        
        # Log final statistics
        logging.info("\n=== Processing Summary ===")
        logging.info(f"Total objects processed: {total_objects}")
        logging.info(f"Total events processed: {total_events:,}")
        logging.info(f"Total processing time: {total_time:.2f} seconds")
        logging.info(f"Average processing rate: {total_objects/total_time:.2f} objects/second")
        logging.info(f"Average event rate: {total_events/total_time:.2f} events/second")
        logging.info(f"Input size: {input_size:.2f} GB")
        if output_size > 0:
            logging.info(f"Output size: {output_size:.2f} GB")
            logging.info(f"Size reduction: {size_reduction_pct:.2f}%")
        logging.info(f"Total size reduction: {total_size_reduction/1024/1024/1024:.2f}GB")
        logging.info(f"Average reduction per object: {(total_size_reduction/total_objects)/1024:.2f}KB")
        logging.info("\nFinal memory state:")
        log_memory_stats()
        
    except Exception as e:
        logging.error(f"Error processing file: {str(e)}")
        logging.error("Stack trace:", exc_info=True)
        raise

def write_chunk(chunk, output_file, is_first_chunk):
    """Write a chunk of results to the output file."""
    mode = 'w' if is_first_chunk else 'a'
    chunk_size = sum(sys.getsizeof(str(obj)) for obj in chunk) / 1024 / 1024  # MB
    
    logging.info(f"Writing chunk to disk (size: {chunk_size:.2f} MB)")
    try:
        with open(output_file, mode) as f:
            if not is_first_chunk:
                f.write(',\n')
            json.dump(chunk, f)
        logging.info(f"Chunk written successfully ({chunk_size:.2f} MB)")
    except Exception as e:
        logging.error(f"Error writing chunk: {str(e)}")
        raise

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Clean large result files by removing unnecessary data")
    parser.add_argument("input_file", help="Path to the input JSON file")
    parser.add_argument("output_file", help="Path to save the cleaned JSON file")
    parser.add_argument("--chunk-size", type=int, default=10,
                        help="Number of objects to process at once (default: 10)")
    parser.add_argument("--debug", action="store_true",
                        help="Enable debug logging")
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Install psutil if not already installed
    try:
        import psutil
    except ImportError:
        print("Installing required package: psutil")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
        import psutil
    
    process_file(args.input_file, args.output_file, args.chunk_size)

if __name__ == "__main__":
    main() 