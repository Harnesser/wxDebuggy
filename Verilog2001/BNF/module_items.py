# Module Items
#
#
# $Id: module_items.py,v 1.1 2007-08-15 23:52:41 marty Exp $
#

import pyparsing as pyp
import module_instanciations as vmi

__full_implementation__ = False

#A.2.1 Declaration types
__ebnf__ = """
module_item ::=
module_or_generate_item
| port_declaration ;
| { attribute_instance } generated_instantiation
| { attribute_instance } local_parameter_declaration
| { attribute_instance } parameter_declaration
| { attribute_instance } specify_block
| { attribute_instance } specparam_declaration
module_or_generate_item ::=
{ attribute_instance } module_or_generate_item_declaration
| { attribute_instance } parameter_override
| { attribute_instance } continuous_assign
| { attribute_instance } gate_instantiation
| { attribute_instance } udp_instantiation
| { attribute_instance } module_instantiation
| { attribute_instance } initial_construct
| { attribute_instance } always_construct
module_or_generate_item_declaration ::=
net_declaration
| reg_declaration
| integer_declaration
| real_declaration
| time_declaration
| realtime_declaration
| event_declaration
| genvar_declaration
| task_declaration
| function_declaration
non_port_module_item ::=
{ attribute_instance } generated_instantiation
| { attribute_instance } local_parameter_declaration
| { attribute_instance } module_or_generate_item
| { attribute_instance } parameter_declaration
| { attribute_instance } specify_block
| { attribute_instance } specparam_declaration
parameter_override ::= defparam list_of_param_assignments ;
"""


module_or_generate_item = vmi.module_instanciation.setName('Module_or_Generate_Item') # Incomplete

non_port_module_item = module_or_generate_item # Incomplete

module_item = module_or_generate_item # Incomplete
 
