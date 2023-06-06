package com.stimulsoft.js;

/**
 * <P>
 * The class that defines the constants that are used to identify generic SQL types, called JDBC
 * types.
 * <p>
 * This class is never instantiated.
 */
public class StiSqlTypes {
    /**
     * <P>
     * The constant in the Java programming language, sometimes referred to as a type code, that
     * identifies the generic SQL type <code>BIT</code>.
     */
    public static final int BIT = -7;

    /**
     * <P>
     * The constant in the Java programming language, sometimes referred to as a type code, that
     * identifies the generic SQL type <code>TINYINT</code>.
     */
    public static final int TINYINT = -6;

    /**
     * <P>
     * The constant in the Java programming language, sometimes referred to as a type code, that
     * identifies the generic SQL type <code>SMALLINT</code>.
     */
    public static final int SMALLINT = 5;

    /**
     * <P>
     * The constant in the Java programming language, sometimes referred to as a type code, that
     * identifies the generic SQL type <code>INTEGER</code>.
     */
    public static final int INTEGER = 4;

    /**
     * <P>
     * The constant in the Java programming language, sometimes referred to as a type code, that
     * identifies the generic SQL type <code>BIGINT</code>.
     */
    public static final int BIGINT = -5;

    /**
     * <P>
     * The constant in the Java programming language, sometimes referred to as a type code, that
     * identifies the generic SQL type <code>FLOAT</code>.
     */
    public static final int FLOAT = 6;

    /**
     * <P>
     * The constant in the Java programming language, sometimes referred to as a type code, that
     * identifies the generic SQL type <code>REAL</code>.
     */
    public static final int REAL = 7;

    /**
     * <P>
     * The constant in the Java programming language, sometimes referred to as a type code, that
     * identifies the generic SQL type <code>DOUBLE</code>.
     */
    public static final int DOUBLE = 8;

    /**
     * <P>
     * The constant in the Java programming language, sometimes referred to as a type code, that
     * identifies the generic SQL type <code>NUMERIC</code>.
     */
    public static final int NUMERIC = 2;

    /**
     * <P>
     * The constant in the Java programming language, sometimes referred to as a type code, that
     * identifies the generic SQL type <code>DECIMAL</code>.
     */
    public static final int DECIMAL = 3;

    /**
     * <P>
     * The constant in the Java programming language, sometimes referred to as a type code, that
     * identifies the generic SQL type <code>CHAR</code>.
     */
    public static final int CHAR = 1;

    /**
     * <P>
     * The constant in the Java programming language, sometimes referred to as a type code, that
     * identifies the generic SQL type <code>VARCHAR</code>.
     */
    public static final int VARCHAR = 12;

    /**
     * <P>
     * The constant in the Java programming language, sometimes referred to as a type code, that
     * identifies the generic SQL type <code>LONGVARCHAR</code>.
     */
    public static final int LONGVARCHAR = -1;

    /**
     * <P>
     * The constant in the Java programming language, sometimes referred to as a type code, that
     * identifies the generic SQL type <code>DATE</code>.
     */
    public static final int DATE = 91;

    /**
     * <P>
     * The constant in the Java programming language, sometimes referred to as a type code, that
     * identifies the generic SQL type <code>TIME</code>.
     */
    public static final int TIME = 92;

    /**
     * <P>
     * The constant in the Java programming language, sometimes referred to as a type code, that
     * identifies the generic SQL type <code>TIMESTAMP</code>.
     */
    public static final int TIMESTAMP = 93;

    public static final int TIMESTAMP_WITH_ZONE = -101;

    /**
     * <P>
     * The constant in the Java programming language, sometimes referred to as a type code, that
     * identifies the generic SQL type <code>BINARY</code>.
     */
    public static final int BINARY = -2;

    /**
     * <P>
     * The constant in the Java programming language, sometimes referred to as a type code, that
     * identifies the generic SQL type <code>VARBINARY</code>.
     */
    public static final int VARBINARY = -3;

    /**
     * <P>
     * The constant in the Java programming language, sometimes referred to as a type code, that
     * identifies the generic SQL type <code>LONGVARBINARY</code>.
     */
    public static final int LONGVARBINARY = -4;

    /**
     * <P>
     * The constant in the Java programming language that identifies the generic SQL value
     * <code>NULL</code>.
     */
    public static final int NULL = 0;

    /**
     * The constant in the Java programming language that indicates that the SQL type is
     * database-specific and gets mapped to a Java object that can be accessed via the methods
     * <code>getObject</code> and <code>setObject</code>.
     */
    public static final int OTHER = 1111;

    /**
     * The constant in the Java programming language, sometimes referred to as a type code, that
     * identifies the generic SQL type <code>JAVA_OBJECT</code>.
     * 
     * @since 1.2
     */
    public static final int JAVA_OBJECT = 2000;

    /**
     * The constant in the Java programming language, sometimes referred to as a type code, that
     * identifies the generic SQL type <code>DISTINCT</code>.
     * 
     * @since 1.2
     */
    public static final int DISTINCT = 2001;

    /**
     * The constant in the Java programming language, sometimes referred to as a type code, that
     * identifies the generic SQL type <code>STRUCT</code>.
     * 
     * @since 1.2
     */
    public static final int STRUCT = 2002;

    /**
     * The constant in the Java programming language, sometimes referred to as a type code, that
     * identifies the generic SQL type <code>ARRAY</code>.
     * 
     * @since 1.2
     */
    public static final int ARRAY = 2003;

    /**
     * The constant in the Java programming language, sometimes referred to as a type code, that
     * identifies the generic SQL type <code>BLOB</code>.
     * 
     * @since 1.2
     */
    public static final int BLOB = 2004;

    /**
     * The constant in the Java programming language, sometimes referred to as a type code, that
     * identifies the generic SQL type <code>CLOB</code>.
     * 
     * @since 1.2
     */
    public static final int CLOB = 2005;

    /**
     * The constant in the Java programming language, sometimes referred to as a type code, that
     * identifies the generic SQL type <code>REF</code>.
     * 
     * @since 1.2
     */
    public static final int REF = 2006;

    /**
     * The constant in the Java programming language, somtimes referred to as a type code, that
     * identifies the generic SQL type <code>DATALINK</code>.
     * 
     * @since 1.4
     */
    public static final int DATALINK = 70;

    /**
     * The constant in the Java programming language, somtimes referred to as a type code, that
     * identifies the generic SQL type <code>BOOLEAN</code>.
     * 
     * @since 1.4
     */
    public static final int BOOLEAN = 16;

    // ------------------------- JDBC 4.0 -----------------------------------

    /**
     * The constant in the Java programming language, sometimes referred to as a type code, that
     * identifies the generic SQL type <code>ROWID</code>
     * 
     * @since 1.6
     * 
     */
    public static final int ROWID = -8;

    /**
     * The constant in the Java programming language, sometimes referred to as a type code, that
     * identifies the generic SQL type <code>NCHAR</code>
     * 
     * @since 1.6
     */
    public static final int NCHAR = -15;

    /**
     * The constant in the Java programming language, sometimes referred to as a type code, that
     * identifies the generic SQL type <code>NVARCHAR</code>.
     * 
     * @since 1.6
     */
    public static final int NVARCHAR = -9;

    /**
     * The constant in the Java programming language, sometimes referred to as a type code, that
     * identifies the generic SQL type <code>LONGNVARCHAR</code>.
     * 
     * @since 1.6
     */
    public static final int LONGNVARCHAR = -16;

    /**
     * The constant in the Java programming language, sometimes referred to as a type code, that
     * identifies the generic SQL type <code>NCLOB</code>.
     * 
     * @since 1.6
     */
    public static final int NCLOB = 2011;

    /**
     * The constant in the Java programming language, sometimes referred to as a type code, that
     * identifies the generic SQL type <code>XML</code>.
     * 
     * @since 1.6
     */
    public static final int SQLXML = 2009;
    /**
     * Oracle ref cursor
     */
    public static final int CURSOR = 121;

    // public static final Hashtable<String, V>

    // Prevent instantiation
    private StiSqlTypes() {
    }
}
