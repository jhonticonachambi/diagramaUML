# # app/application/services/csharp_to_plantuml_converter.py
import re
from typing import List, Dict, Tuple

class CSharpToPlantUMLConverter:
    def __init__(self):
        self.classes: Dict[str, Dict] = {}
        self.relationships: List[Tuple] = []
        self.current_class = None

    def convert(self, code: str) -> str:
        # Preprocesamiento
        code = self._remove_comments(code)
        code = self._remove_string_literals(code)
        
        # Detección de elementos
        self._detect_inheritance(code)
        self._detect_classes(code)
        self._detect_relationships(code)
        
        # Generación UML
        uml = ['@startuml']
        uml.extend(self._generate_classes_uml())
        uml.extend(self._generate_relationships_uml())
        uml.append('@enduml')
        
        return '\n'.join(uml)

    def _remove_comments(self, code: str) -> str:
        code = re.sub(r'//.*', '', code)  # Comentarios de una línea
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)  # Comentarios multilínea
        return code

    def _remove_string_literals(self, code: str) -> str:
        return re.sub(r'"[^"]*"', '""', code)

    def _detect_classes(self, code: str):
        class_pattern = re.compile(
            r'(?:public\s+|private\s+|protected\s+|internal\s+|abstract\s+|sealed\s+)*class\s+(\w+)(?:\s*:\s*([\w<>,\s]+))?\s*\{',
            re.MULTILINE
        )
        
        for match in class_pattern.finditer(code):
            class_name = match.group(1)
            base_classes = match.group(2).split(',') if match.group(2) else []
            
            self.classes[class_name] = {
                'properties': [],
                'fields': [],
                'methods': [],
                'base_classes': [bc.strip() for bc in base_classes],
                'is_abstract': 'abstract' in match.group(0)
            }
            
            start_index = match.end()
            class_body = self._extract_class_body(code[start_index:])
            self._parse_class_members(class_name, class_body)

    def _parse_class_members(self, class_name: str, class_body: str):
        property_pattern = re.compile(
            r'(public|private|protected|internal)\s+([\w<>,\s]+)\s+(\w+)\s*\{[^}]*\}',
            re.DOTALL
        )
        
        field_pattern = re.compile(
            r'(public|private|protected|internal)\s+([\w<>,\s]+)\s+(\w+)\s*[;=]',
            re.MULTILINE
        )
        
        method_pattern = re.compile(
            r'(public|private|protected|internal|abstract|virtual|override)\s+([\w<>,\s]+)\s+(\w+)\s*\((.*?)\)\s*\{?',
            re.DOTALL
        )
        
        for match in property_pattern.finditer(class_body):
            vis, type_, name = match.groups()
            self.classes[class_name]['properties'].append({
                'visibility': vis,
                'type': type_.strip(),
                'name': name
            })
        
        for match in field_pattern.finditer(class_body):
            vis, type_, name = match.groups()
            self.classes[class_name]['fields'].append({
                'visibility': vis,
                'type': type_.strip(),
                'name': name
            })
        
        for match in method_pattern.finditer(class_body):
            modifiers, ret_type, name, params = match.groups()
            vis = next((m for m in modifiers.split() if m in ['public', 'private', 'protected', 'internal']), 'private')
            self.classes[class_name]['methods'].append({
                'visibility': vis,
                'return_type': ret_type.strip(),
                'name': name,
                'parameters': self._parse_parameters(params),
                'is_abstract': 'abstract' in modifiers,
                'is_virtual': 'virtual' in modifiers,
                'is_override': 'override' in modifiers
            })

    def _parse_parameters(self, param_str: str) -> List[Dict]:
        params = []
        for p in param_str.split(','):
            p = p.strip()
            if not p:
                continue
            parts = re.split(r'\s+', p)
            if len(parts) >= 2:
                type_ = ' '.join(parts[:-1])
                name = parts[-1]
                params.append({'type': type_, 'name': name})
        return params

    def _detect_inheritance(self, code: str):
        # Ya detectado en _detect_classes
        pass

    def _detect_relationships(self, code: str):
        # Detectar relaciones de agregación/composición
        for class_name, class_info in self.classes.items():
            # Por propiedades/fields
            for member in class_info['properties'] + class_info['fields']:
                member_type = member['type']
                if member_type in self.classes:
                    self.relationships.append((
                        class_name,
                        member_type,
                        'association',
                        f'"{member["name"]}"'
                    ))
            
            # Por parámetros de métodos
            for method in class_info['methods']:
                for param in method['parameters']:
                    if param['type'] in self.classes:
                        self.relationships.append((
                            class_name,
                            param['type'],
                            'dependency',
                            f'"{method["name"]}()"'
                        ))

    def _extract_class_body(self, code_after_class: str) -> str:
        depth = 1
        body = []
        for char in code_after_class:
            if char == '{':
                depth += 1
            elif char == '}':
                depth -= 1
                if depth == 0:
                    break
            body.append(char)
        return ''.join(body)

    def _generate_classes_uml(self) -> List[str]:
        uml = []
        for class_name, class_info in self.classes.items():
            class_decl = f'{"abstract " if class_info["is_abstract"] else ""}class {class_name}'
            if class_info['base_classes']:
                class_decl += f' extends {", ".join(class_info["base_classes"])}'
            
            uml.append(class_decl + ' {')
            
            for field in class_info['fields']:
                vis_symbol = self._vis_to_symbol(field['visibility'])
                uml.append(f'    {vis_symbol}{field["name"]} : {field["type"]}')
            
            for prop in class_info['properties']:
                vis_symbol = self._vis_to_symbol(prop['visibility'])
                uml.append(f'    {vis_symbol}{prop["name"]} : {prop["type"]}')
            
            for method in class_info['methods']:
                vis_symbol = self._vis_to_symbol(method['visibility'])
                params = ', '.join(f'{p["name"]} : {p["type"]}' for p in method['parameters'])
                modifiers = []
                if method['is_abstract']: modifiers.append('abstract')
                if method['is_virtual']: modifiers.append('virtual')
                if method['is_override']: modifiers.append('override')
                modifier_str = f' {{{",".join(modifiers)}}}' if modifiers else ''
                uml.append(f'    {vis_symbol}{method["name"]}({params}) : {method["return_type"]}{modifier_str}')
            
            uml.append('}')
        return uml

    def _generate_relationships_uml(self) -> List[str]:
        relationships = []
        
        # Herencia
        for class_name, class_info in self.classes.items():
            for base_class in class_info['base_classes']:
                if base_class in self.classes:
                    relationships.append(f'{base_class} <|-- {class_name}')
        
        # Otras relaciones
        for rel in self.relationships:
            source, target, rel_type, label = rel
            if rel_type == 'association':
                relationships.append(f'{source} --> {label} {target}')
            elif rel_type == 'dependency':
                relationships.append(f'{source} ..> {label} {target}')
        
        return relationships

    def _vis_to_symbol(self, vis: str) -> str:
        return {
            'public': '+',
            'private': '-',
            'protected': '#',
            'internal': '~'
        }.get(vis.lower(), '~')

