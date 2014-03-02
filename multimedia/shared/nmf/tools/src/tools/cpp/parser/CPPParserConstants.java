/*
 * Copyright (C) ST-Ericsson SA 2010. All rights reserved.
 *
 * This code is part of the NMF Toolset.
 *
 * The NMF Toolset is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * The NMF Toolset is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with the NMF Toolset. If not, see <http://www.gnu.org/licenses/>.
 *
 */
/* Generated By:JavaCC: Do not edit this line. CPPParserConstants.java */
package tools.cpp.parser;


/**
 * Token literal values and constants.
 * Generated by org.javacc.parser.OtherFilesGen#start()
 */
public interface CPPParserConstants {

  /** End of File. */
  int EOF = 0;
  /** RegularExpression Id. */
  int POUND_INCLUDE = 5;
  /** RegularExpression Id. */
  int TEXT = 6;
  /** RegularExpression Id. */
  int ABS_INCLUDE = 9;
  /** RegularExpression Id. */
  int REL_INCLUDE = 10;
  /** RegularExpression Id. */
  int ENDINCLUDE = 11;

  /** Lexical state. */
  int DEFAULT = 0;
  /** Lexical state. */
  int PREPROCESSOR_OUTPUT = 1;

  /** Literal token values. */
  String[] tokenImage = {
    "<EOF>",
    "\" \"",
    "\"\\t\"",
    "\"\\r\\n\"",
    "\"\\n\"",
    "<POUND_INCLUDE>",
    "<TEXT>",
    "\" \"",
    "\"\\t\"",
    "<ABS_INCLUDE>",
    "<REL_INCLUDE>",
    "<ENDINCLUDE>",
  };

}